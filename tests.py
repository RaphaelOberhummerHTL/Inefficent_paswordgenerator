import collections
import math
import unittest
import scipy.stats as stats
# It's testing the multithreading
import threading
from queue import Queue

import passwordgenerator
import translationchaos


class TestPasswordLengthAndLimits(unittest.TestCase):
    """Verifies the strictly deterministic boundary limits and fallback constraints of the password generator."""

    def setUp(self):
        """Initializes the baseline environmental constants for deterministic test execution."""
        self.default_prompt: str = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        self.default_keywords: str = "morgen; Supermarkt; Abendessen"

    def test_password_length_variants(self):
        """
        Validates whether the entropy engine strictly adheres to desired length configurations
        or triggers predefined structural fallbacks when fed out-of-bounds metrics.
        """
        # Valid length bounds: Ensure the output matrix directly scales with requested dimensions
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, 10)), 10)
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, 30)), 30)

        # Default values and catastrophic boundary recovery (expected default fallback: 20 characters)
        # CRITICAL: Ensures the system defaults to 20 when length arguments are omitted, negative, or absurdly low
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords)), 20)
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, 2)), 20)
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, 0)), 20)
        self.assertEqual(len(passwordgenerator.password(self.default_prompt, 1, "Slice of Life", self.default_keywords, -20)), 20)


class TestPasswordStatisticalBias(unittest.TestCase):
    """
    Extracts a monolithic, single-pass batch matrix of 300 passwords to mathematically 
    interrogate the generator for structural, positional, or algorithmic biases.
    
    Optimized via setUpClass to mitigate devastating local LLM inference overhead and 
    prevent the AI from melting the user's GPU during repetitive sampling loops.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Deploys a multi-threaded (conceptually) heavy inference batch generation process 
        to compile the necessary data pool for cryptographic and mathematical scrutiny.
        """
        prompt: str = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        keywords: str = "morgen; Abendessen; frisches"
        
        # A sample depth of 300 iterations is large enough to expose only large, obvious 
        # flaws: strong character clustering, heavy positional bias, or a fast entropy 
        # collapse. It is NOT large enough to rule out subtler structural bias, and it 
        # says nothing about whether the underlying generation algorithm is cryptographically 
        # safe — that requires analyzing the seed space, not sampling the output.
        cls.passwords: list[str] = [
            passwordgenerator.password(prompt, 2, "Slice of Life", keywords, 10)
            for _ in range(300)
        ]

    def test_character_frequency_bias(self):
        """
        Performs a rigorous Pearson's Chi-Squared test across the entire flattened string matrix.
        Validates if the distribution of characters deviates from a perfect uniform distribution.
        """
        all_chars: str = "".join(self.passwords)
        char_counts = collections.Counter(all_chars)
        
        total_chars: int = len(all_chars)
        unique_chars_found: int = len(char_counts)
        expected_freq: float = total_chars / unique_chars_found
        
        # Flatten empirical observations and compare against the isotropic ideal expectation
        observed: list[int] = list(char_counts.values())
        expected: list[float] = [expected_freq] * unique_chars_found
        
        _, p_value = stats.chisquare(observed, f_exp=expected)
        
        # CRITICAL: A p-value below 0.01 indicates significant algorithmic predictable clustering!
        self.assertGreater(p_value, 0.01, "The Passwordgenerator shows a significant character bias!")

    def test_positional_bias(self):
        """
        Interrogates the absolute starting index (Index 0) of all generated passphrases.
        Ensures that the rolling mathematical polynomial equations do not exhibit 
        gravitational pull towards specific character categories at the structural frontier.
        """
        first_chars: list[str] = [pw[0] for pw in self.passwords if pw]
        total_pws: int = len(self.passwords)
        
        # Threshold set to 60% as the sample size is intentionally finite and bounded, 
        # preventing false positives caused by chaotic linguistic fluctuations.
        
        # Evaluating Alphabetic Uppercase Dominance
        uppercase_start: int = sum(1 for c in first_chars if c.isupper())
        ratio: float = uppercase_start / total_pws
        self.assertLess(ratio, 0.60, f"Structural bias: {ratio*100}% start with an uppercase letter.")
        
        # Evaluating Alphabetic Lowercase Dominance
        lowercase_start: int = sum(1 for c in first_chars if c.islower())
        ratio = lowercase_start / total_pws
        self.assertLess(ratio, 0.60, f"Structural bias: {ratio*100}% start with a lowercase letter.")

        # Evaluating Numeric Digit Dominance
        digits_start: int = sum(1 for c in first_chars if c.isdigit())
        ratio = digits_start / total_pws
        self.assertLess(ratio, 0.60, f"Structural bias: {ratio*100}% start with a digit.")

        # Evaluating Esoteric Non-Alphanumeric Glyphs
        special_characters: list[str] = [
            '.', ':', '-', '_', ',', ';', '#', '\'', '+', '*', '’', '~', '´', '`', 
            '<', '>', '|', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '{', 
            '}', '[', ']', '^', '°', '\\'
        ]
        special_start: int = sum(1 for c in first_chars if c in special_characters)
        ratio = special_start / total_pws
        self.assertLess(ratio, 0.60, f"Structural bias: {ratio*100}% start with a special character.")

    def test_shannon_entropy_bias(self):
        """
        Calculates the internal Shannon Entropy of individual strings to certify 
        high-dimensional information density. Prevents predictable text repeating.
        """
        def _shannon(password: str) -> float | int:
            if not password:
                return 0
            total_len: int = len(password)
            counts = collections.Counter(password)
            # Mathematical implementation of standard information-theoretic Shannon formula
            return -sum((count / total_len) * math.log2(count / total_len) for count in counts.values())

        avg_entropy: float = sum(_shannon(pw) for pw in self.passwords) / len(self.passwords)
        
        # Distributional check only: flags passwords with heavily repeated/skewed characters
        self.assertGreater(avg_entropy, 4.1, f"Entropy too low to be cryptographically secure: {avg_entropy}")

    def test_password_distribution_entropy(self):
        """
        Analyzes the macroscopic Shannon Entropy across the entire generated password ecosystem.
        If the LLM translation decay pipeline degrades into deterministic loops, 
        macro-entropy collapses, causing severe collisions.
        """
        total_pws: int = len(self.passwords)
        # Quantify recurring patterns inside the macro population matrix
        pw_counts = collections.Counter(self.passwords)
        
        # Execute global entropy summation
        entropy: float = -sum(
            (count / total_pws) * math.log2(count / total_pws) 
            for count in pw_counts.values()
        )
        
        # Theoretical maximum entropy for N uniquely discrete elements equals log2(N)
        max_entropy: float = math.log2(total_pws)
        
        # Tolerance limit: The system must retain at least 95% of absolute maximum chaos
        min_expected_entropy: float = max_entropy * 0.95
        
        self.assertGreater(
            entropy, 
            min_expected_entropy, 
            f"Insufficient entropy across the macro password population: {entropy:.2f} Bits. "
            f"(Maximum theoretical yield: {max_entropy:.2f} Bits, Required threshold: >{min_expected_entropy:.2f} Bits). "
            f"The matrix suffers from an excess of identical duplication vectors!"
        )

    def test_password_uniqueness_ratio(self):
        """
        Measures the absolute uniqueness ratio of the generated dataset.
        Triggers an explicit human-readable cryptographic alert if the system is caught 
        generating duplicate outputs due to deterministic seeding traps.
        """
        total_pws: int = len(self.passwords)
        unique_pws: int = len(set(self.passwords))
        ratio: float = unique_pws / total_pws
        
        # Strict requirement: Less than 2% collision allowance under severe multi-language corruption
        min_allowed_ratio: float = 0.98
        
        self.assertGreater(
            ratio, 
            min_allowed_ratio, 
            f"Catastrophic collision rate detected! Only {unique_pws} out of {total_pws} "
            f"passwords are structurally unique ({ratio * 100:.1f}%). "
            f"Expected minimum threshold was {min_allowed_ratio * 100:.1f}%."
        )

class TestPasswordMultithreading(unittest.TestCase):
    """Verifies the stability and entropy generation under concurrent thread execution."""

    def test_concurrent_password_generation(self):
        """
        Launches two concurrent threads to generate passwords simultaneously.
        Validates structural stability and tests for dynamic seed-state divergence 
        caused by thread interleaving.
        """
        result_queue = Queue()
        prompt: str = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        keywords: str = "morgen; Supermarkt; Abendessen; frisches"

        # Worker function execution block for threads
        def thread_worker(target_length: int):
            try:
                pw = passwordgenerator.password(prompt, 1, "Slice of Life", keywords, target_length)
                result_queue.put(pw)
            except Exception as e:
                result_queue.put(e)  # Catch hardware/ollama failures to prevent thread deadlocks

        # Define and initialize two concurrent worker threads targeting a length of 10
        thread1 = threading.Thread(target=thread_worker, args=(10,))
        thread2 = threading.Thread(target=thread_worker, args=(10,))

        # Fire threads into execution context
        thread1.start()
        thread2.start()

        # Await completion of both concurrent cryptographic/LLM pipelines
        thread1.join()
        thread2.join()

        # Extract elements from the thread-safe queue matrix
        pw1 = result_queue.get()
        pw2 = result_queue.get()

        # CRITICAL: Verify that neither thread crashed due to race conditions or Ollama locks
        self.assertNotIsInstance(pw1, Exception, f"Thread 1 crashed with an internal exception: {pw1}")
        self.assertNotIsInstance(pw2, Exception, f"Thread 2 crashed with an internal exception: {pw2}")

        # Validate that thread-interleaving prevented a deterministic state collision
        self.assertNotEqual(pw1, pw2, "Critical Failure: Threads generated identical passwords! Entropy space collapsed.")

class TestTranslations(unittest.TestCase):
    """Audits the linguistic chaos pipeline for volatile edge-case tolerance, text drift, and error deflection."""

    def setUp(self):
        """Constructs semantic baselines containing varied linguistic patterns (German, English, Hybrid Code-Switching)."""
        self.de_prompt = "Ich gehe morgen in den Supermarkt und kaufe etwas frisches Gemüse für das Abendessen."
        self.en_prompt = "I am going to the supermarket tomorrow and buying some fresh vegetables for dinner."
        self.mix_prompt = "Ich gehe morgen to the supermarket und kaufe some fresh vegetables für das Abendessen."

    def test_translation_layers_structural_change(self):
        """
        Verifies that sufficient iterative loops introduce cascading semantic decay.
        The text must warp far enough to prevent the output from matching the original state string.
        """
        # A 10-round multi-language cascade must trigger significant linguistic drift
        self.assertNotEqual(translationchaos.translation_chaos(self.de_prompt, 10, "German"), self.de_prompt)
        self.assertNotEqual(translationchaos.translation_chaos(self.en_prompt, 10, "German"), self.de_prompt)
        self.assertNotEqual(translationchaos.translation_chaos(self.mix_prompt, 10, "German"), self.de_prompt)

    def test_translation_one_round_noop(self):
        """
        Validates the mathematical No-Operation (NoOp) identity property of the translation stack.
        A single translation loop targeting the input text's native tongue should theoretically yield an identical string.
        """
        self.assertEqual(translationchaos.translation_chaos(self.de_prompt, 1, "German"), self.de_prompt)

    def test_translation_invalid_rounds_raise_error(self):
        """
        Asserts that entering non-Euclidean or negative iteration cycles correctly 
        triggers a protective, hardware-saving ValueError.
        """
        with self.assertRaises(ValueError):
            translationchaos.translation_chaos(self.de_prompt, -10, "German")
        with self.assertRaises(ValueError):
            translationchaos.randimasation_through_translation(self.de_prompt, -10)

    def test_translation_empty_inputs_raise_error(self):
        """
        Ensures that feeding vacuum, zero-length, or whitespace-only inputs into 
        the neural network interface instantly throws an exception instead of spinning into an infinite void.
        """
        for empty_input in ["", "   ", "            "]:
            with self.assertRaises(ValueError):
                translationchaos.translation_chaos(empty_input, 10, "German")
            with self.assertRaises(ValueError):
                translationchaos.randimasation_through_translation(empty_input, 10)

    def test_random_translation_path(self):
        """
        Validates the untethered stochastic execution path.
        Forcing random hops without a fixed language terminal must result in absolute, irreversible textual divergence.
        """
        self.assertNotEqual(translationchaos.randimasation_through_translation(self.de_prompt, 10), self.de_prompt)


if __name__ == '__main__':
    # Initialize the unit testing framework to execute the hyper-inefficient validation suite
    unittest.main()