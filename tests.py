import collections
import math
import unittest
import scipy.stats as stats

import passwordgenerator
import translationchaos


class TestPasswordLengthAndLimits(unittest.TestCase):
    """Tests the deterministic length limits of the password generator."""

    def setUp(self):
        self.default_prompt = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        self.default_keywords = "morgen; Supermarkt; Abendessen"

    def test_password_length_variants(self):
        # Valid lengths
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, 10)), 10)
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, 30)), 30)

        # Default values and fallbacks for invalid lengths (expected default: 20)
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords)), 20)
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, 2)), 20)
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, 0)), 20)
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, -20)), 20)


class TestPasswordStatisticalBias(unittest.TestCase):
    """
    Collects a one-time sample of passwords to test for statistical bias.
    Uses setUpClass to prevent the AI from regenerating passwords for every single test.
    """

    @classmethod
    def setUpClass(cls):
        print("\n--> Generating sample for bias tests (300 passwords)...")
        prompt = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        keywords = "morgen; Abendessen; frisches"
        
        # For mathematical significance in passwords, 300 should be sufficient 
        # for a rough overview of the entropy and structural bias.
        cls.passwords = [
            passwordgenerator.password(prompt, 2, "Slice of Life", keywords, 10)
            for _ in range(300)
        ]

    def test_character_frequency_bias(self):
        all_chars = "".join(self.passwords)
        char_counts = collections.Counter(all_chars)
        
        total_chars = len(all_chars)
        unique_chars_found = len(char_counts)
        expected_freq = total_chars / unique_chars_found
        
        observed = list(char_counts.values())
        expected = [expected_freq] * unique_chars_found
        
        _, p_value = stats.chisquare(observed, f_exp=expected)
        self.assertGreater(p_value, 0.01, "AI shows a significant character bias!")

    def test_positional_bias(self):
        first_chars = [pw[0] for pw in self.passwords if pw]
        uppercase_start = sum(1 for c in first_chars if c.isupper())
        ratio = uppercase_start / len(self.passwords)
        
        self.assertLess(ratio, 0.80, f"Structural bias: {ratio*100}% start with an uppercase letter.")

    def test_shannon_entropy_bias(self):
        def _shannon(password):
            if not password: return 0
            total_len = len(password)
            counts = collections.Counter(password)
            return -sum((count / total_len) * math.log2(count / total_len) for count in counts.values())

        avg_entropy = sum(_shannon(pw) for pw in self.passwords) / len(self.passwords)
        self.assertGreater(avg_entropy, 2.5, f"Entropy too low: {avg_entropy}")


class TestTranslations(unittest.TestCase):
    """Tests the linguistic chaos pipeline for edge cases and error handling."""

    def setUp(self):
        self.de_prompt = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        self.en_prompt = "I am going to the supermarket tomorrow and buying some fresh vegetables for dinner."
        self.mix_prompt = "Ich gehe morgen to the supermarket und kaufe some fresh vegetables für das Abendessen."

    def test_translation_layers_structural_change(self):
        # 10 rounds should definitely alter the text
        self.assertNotEqual(translationchaos.translation_chaos(self.de_prompt, 10, "German"), self.de_prompt)
        self.assertNotEqual(translationchaos.translation_chaos(self.en_prompt, 10, "German"), self.de_prompt)
        self.assertNotEqual(translationchaos.translation_chaos(self.mix_prompt, 10, "German"), self.de_prompt)

    def test_translation_one_round_noop(self):
        # 1 round from German to German should (theoretically) remain identical
        self.assertEqual(translationchaos.translation_chaos(self.de_prompt, 1, "German"), self.de_prompt)

    def test_translation_invalid_rounds_raise_error(self):
        with self.assertRaises(ValueError):
            translationchaos.translation_chaos(self.de_prompt, -10, "German")
        with self.assertRaises(ValueError):
            translationchaos.randimasation_through_translation(self.de_prompt, -10)

    def test_translation_empty_inputs_raise_error(self):
        for empty_input in ["", "   ", "            "]:
            with self.assertRaises(ValueError):
                translationchaos.translation_chaos(empty_input, 10, "German")
            with self.assertRaises(ValueError):
                translationchaos.randimasation_through_translation(empty_input, 10)

    def test_random_translation_path(self):
        # Tests the function without a fixed target language
        self.assertNotEqual(translationchaos.randimasation_through_translation(self.de_prompt, 10), self.de_prompt)


if __name__ == '__main__':
    unittest.main()