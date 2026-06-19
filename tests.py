import collections
import math
import unittest
import scipy.stats as stats

import passwordgenerator
import translationchaos


class TestPasswordLengthAndLimits(unittest.TestCase):
    """Tests the deterministic length limits of the password generator."""

    def setUp(self):
        self.default_prompt: str = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        self.default_keywords: str = "morgen; Supermarkt; Abendessen"

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
    def setUpClass(cls) -> None:
        print("\n--> Generating sample for bias tests (300 passwords)...")
        prompt: str = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        keywords: str = "morgen; Abendessen; frisches"
        
        # For mathematical significance in passwords, 300 should be sufficient 
        # for a rough overview of the entropy and structural bias.
        cls.passwords: list[str] = [
            passwordgenerator.password(prompt, 2, "Slice of Life", keywords, 10)
            for _ in range(300)
        ]

    def test_character_frequency_bias(self):
        all_chars: str = "".join(self.passwords)
        char_counts = collections.Counter(all_chars)
        
        total_chars: int = len(all_chars)
        unique_chars_found: int = len(char_counts)
        expected_freq: float = total_chars / unique_chars_found
        
        observed: list[int] = list(char_counts.values())
        expected: list[float] = [expected_freq] * unique_chars_found
        
        _, p_value = stats.chisquare(observed, f_exp=expected)
        self.assertGreater(p_value, 0.01, "The Passwordgenerator shows a significant character bias!")

    def test_positional_bias(self):
        first_chars: list[str] = [pw[0] for pw in self.passwords if pw]
        total_pws: int = len(self.passwords)
        
        # I use the probability from 60% because the sample size is too small to be around the optimal probability for each set of characters
        uppercase_start: int = sum(1 for c in first_chars if c.isupper())
        ratio: float = uppercase_start / total_pws
        self.assertLess(ratio, 0.60, f"Structural bias: {ratio*100}% start with an uppercase letter.")
        
        lowercase_start: int = sum(1 for c in first_chars if c.islower())
        ratio = lowercase_start / total_pws
        self.assertLess(ratio, 0.60, f"Structural bias: {ratio*100}% start with a lowercase letter.")

        digits_start: int = sum(1 for c in first_chars if c.isdigit())
        ratio = digits_start / total_pws
        self.assertLess(ratio, 0.60, f"Structural bias: {ratio*100}% start with a digit.")

        special_characters: list[str] = [
            '.', ':', '-', '_', ',', ';', '#', '\'', '+', '*', '’', '~', '´', '`', 
            '<', '>', '|', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '{', 
            '}', '[', ']', '^', '°', '\\'
        ]
        special_start: int = sum(1 for c in first_chars if c in special_characters)
        ratio = special_start / total_pws
        self.assertLess(ratio, 0.60, f"Structural bias: {ratio*100}% start with a special character.")

    def test_shannon_entropy_bias(self):
        def _shannon(password: str) -> float | int:
            if not password:
                return 0
            total_len: int = len(password)
            counts = collections.Counter(password)
            return -sum((count / total_len) * math.log2(count / total_len) for count in counts.values())

        avg_entropy: float = sum(_shannon(pw) for pw in self.passwords) / len(self.passwords)
        self.assertGreater(avg_entropy, 2.5, f"Entropy too low: {avg_entropy}")


class TestTranslations(unittest.TestCase):
    """Tests the linguistic chaos pipeline for edge cases and error handling."""

    def setUp(self):
        self.de_prompt = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        self.en_prompt = "I am going to the supermarket tomorrow and buying some fresh vegetables for dinner."
        self.mix_prompt = "Ich gehe morgen to the supermarket und kaufe some fresh vegetables für das Abendessen."

    def test_translation_layers_structural_change(self):
        # 10 rounds should alter the text enough to see a drift in the translation
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