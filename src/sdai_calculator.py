"""
SDAI (Simplified Disease Activity Index) Calculator
A simplified disease activity index for rheumatoid arthritis.

Usage:
    python -m src.sdai_calculator                  # Interactive mode
    python -m src.sdai_calculator --tjc 8 --sjc 6 --pga 5.0 --ega 4.0 --crp 2.5
    python -m src.sdai_calculator --help
"""

import argparse
import sys
from enum import Enum
from typing import Optional


class ActivityCategory(Enum):
    """SDAI disease activity categories."""
    REMISSION = "Remission"
    LOW = "Low Activity"
    MODERATE = "Moderate Activity"
    HIGH = "High Activity"


class SDAICalculator:
    """
    SDAI Index Calculator.

    SDAI = TJC + SJC + PGA + EGA + CRP

    where:
        TJC (Tender Joint Count) — number of tender joints (0–28)
        SJC (Swollen Joint Count) — number of swollen joints (0–28)
        PGA (Patient Global Assessment) — patient global VAS (0–10 cm)
        EGA (Evaluator Global Assessment) — evaluator global VAS (0–10 cm)
        CRP (C-reactive protein) — C-reactive protein level (mg/dL)
    """

    REMISSION_THRESHOLD = 3.3
    LOW_ACTIVITY_THRESHOLD = 11.0
    MODERATE_ACTIVITY_THRESHOLD = 26.0

    def __init__(self):
        """Initialize limits for input parameters."""
        self.limits = {
            "tjc": (0, 28),
            "sjc": (0, 28),
            "pga": (0.0, 10.0),
            "ega": (0.0, 10.0),
            "crp": (0.0, float("inf")),
        }

    def validate_input(self, name: str, value: float) -> None:
        """
        Validate an input value against its allowed range.

        Args:
            name: Parameter name.
            value: Value to validate.

        Raises:
            ValueError: If value is outside the allowed range.
        """
        min_val, max_val = self.limits[name]
        if not (min_val <= value <= max_val):
            raise ValueError(
                f"{name.upper()}: value {value} is outside "
                f"range [{min_val}, {max_val}]."
            )

    def calculate(
        self,
        tjc: int,
        sjc: int,
        pga: float,
        ega: float,
        crp: float,
    ) -> dict:
        """
        Calculate SDAI index and determine activity category.

        Args:
            tjc: Tender joint count (0–28).
            sjc: Swollen joint count (0–28).
            pga: Patient global assessment on VAS (0–10 cm).
            ega: Evaluator global assessment on VAS (0–10 cm).
            crp: C-reactive protein level (mg/dL, >= 0).

        Returns:
            Dictionary with keys:
                - "sdai": calculated index (float).
                - "category": activity category (ActivityCategory).
                - "interpretation": text description (str).

        Raises:
            ValueError: If input data is invalid.
        """
        self.validate_input("tjc", tjc)
        self.validate_input("sjc", sjc)
        self.validate_input("pga", pga)
        self.validate_input("ega", ega)
        self.validate_input("crp", crp)

        sdai_score = tjc + sjc + pga + ega + crp
        sdai_score = round(sdai_score, 1)

        category = self._get_category(sdai_score)

        return {
            "sdai": sdai_score,
            "category": category,
            "interpretation": f"SDAI = {sdai_score} — {category.value}",
        }

    def _get_category(self, score: float) -> ActivityCategory:
        """
        Determine activity category based on SDAI score.

        Args:
            score: SDAI index value.

        Returns:
            Activity category (ActivityCategory).
        """
        if score <= self.REMISSION_THRESHOLD:
            return ActivityCategory.REMISSION
        elif score <= self.LOW_ACTIVITY_THRESHOLD:
            return ActivityCategory.LOW
        elif score <= self.MODERATE_ACTIVITY_THRESHOLD:
            return ActivityCategory.MODERATE
        else:
            return ActivityCategory.HIGH

    def print_detailed_result(
        self, tjc: int, sjc: int, pga: float, ega: float, crp: float
    ) -> None:
        """
        Print a detailed result with component breakdown.

        Args:
            tjc: Tender joint count.
            sjc: Swollen joint count.
            pga: Patient global assessment.
            ega: Evaluator global assessment.
            crp: C-reactive protein level.
        """
        result = self.calculate(tjc, sjc, pga, ega, crp)

        category_colors = {
            ActivityCategory.REMISSION: "\U0001f7e2",  # 🟢
            ActivityCategory.LOW: "\U0001f7e1",         # 🟡
            ActivityCategory.MODERATE: "\U0001f7e0",    # 🟠
            ActivityCategory.HIGH: "\U0001f534",        # 🔴
        }
        indicator = category_colors.get(result["category"], "\u26aa")  # ⚪

        print("\n" + "=" * 55)
        print("                SDAI CALCULATOR")
        print("=" * 55)
        print(f"  Tender Joints (TJC):          {tjc:>10}")
        print(f"  Swollen Joints (SJC):         {sjc:>10}")
        print(f"  Patient Global (PGA):         {pga:>8.1f} cm")
        print(f"  Evaluator Global (EGA):       {ega:>8.1f} cm")
        print(f"  CRP:                          {crp:>8.1f} mg/dL")
        print("-" * 55)
        print(f"  SDAI INDEX:                   {result['sdai']:>8}")
        print(
            f"  CATEGORY:        {indicator} {result['category'].value}"
        )
        print("=" * 55 + "\n")

        self._print_clinical_context(result["category"])

    def _print_clinical_context(self, category: ActivityCategory) -> None:
        """
        Print additional clinical context based on activity category.

        Args:
            category: Activity category.
        """
        contexts = {
            ActivityCategory.REMISSION: (
                "Clinical context: Disease is inactive. "
                "Treatment goal achieved.\n"
                "Consider maintaining current therapy."
            ),
            ActivityCategory.LOW: (
                "Clinical context: Minimal disease activity. "
                "Acceptable level.\n"
                "Continue monitoring, consider therapy adjustment "
                "if not at target."
            ),
            ActivityCategory.MODERATE: (
                "Clinical context: Moderate disease activity.\n"
                "Therapy modification should be considered according to\n"
                "ACR/EULAR recommendations."
            ),
            ActivityCategory.HIGH: (
                "Clinical context: HIGH disease activity. Severe "
                "flare.\n"
                "Aggressive therapy escalation is warranted. Close "
                "monitoring\n"
                "and frequent follow-up are strongly recommended."
            ),
        }
        print(contexts.get(category, ""))


class InteractiveConsole:
    """Handles interactive input mode for clinicians."""

    def __init__(self, calculator: SDAICalculator):
        """
        Initialize the interactive console.

        Args:
            calculator: SDAICalculator instance.
        """
        self.calculator = calculator

    def run(self) -> None:
        """Run the interactive input loop."""
        print("\n" + "=" * 55)
        print("       SDAI CALCULATOR — INTERACTIVE MODE")
        print("=" * 55)
        print("Enter patient data to calculate disease activity.\n")

        while True:
            try:
                tjc = self._prompt_int(
                    "Tender Joint Count (TJC, 0–28): ", min_val=0, max_val=28
                )
                sjc = self._prompt_int(
                    "Swollen Joint Count (SJC, 0–28): ", min_val=0, max_val=28
                )
                pga = self._prompt_float(
                    "Patient Global Assessment (PGA, 0–10 cm): ",
                    min_val=0.0,
                    max_val=10.0,
                )
                ega = self._prompt_float(
                    "Evaluator Global Assessment (EGA, 0–10 cm): ",
                    min_val=0.0,
                    max_val=10.0,
                )
                crp = self._prompt_float(
                    "C-reactive protein (CRP, mg/dL, >= 0): ",
                    min_val=0.0,
                    max_val=None,
                )

                self.calculator.print_detailed_result(
                    tjc, sjc, pga, ega, crp
                )

            except (ValueError, TypeError) as e:
                print(f"\nError: {e}")
                print("Please try again.\n")
                continue

            if not self._prompt_yes_no(
                "\nCalculate another patient? (y/n): "
            ):
                print(
                    "\nThank you for using the SDAI Calculator. "
                    "Goodbye!\n"
                )
                break

    def _prompt_int(
        self, prompt: str, min_val: int, max_val: int
    ) -> int:
        """
        Prompt user for an integer value within range.

        Args:
            prompt: Input prompt string.
            min_val: Minimum allowed value.
            max_val: Maximum allowed value.

        Returns:
            Validated integer value.

        Raises:
            ValueError: If input is not a valid integer or out of range.
        """
        while True:
            try:
                value = int(input(prompt))
                if not (min_val <= value <= max_val):
                    raise ValueError(
                        f"Value must be between {min_val} and "
                        f"{max_val}."
                    )
                return value
            except ValueError as e:
                if "must be between" in str(e):
                    print(f"  ! {e}")
                else:
                    print("  ! Please enter a valid whole number.")
                continue

    def _prompt_float(
        self,
        prompt: str,
        min_val: float,
        max_val: Optional[float],
    ) -> float:
        """
        Prompt user for a float value within range.

        Args:
            prompt: Input prompt string.
            min_val: Minimum allowed value.
            max_val: Maximum allowed value (None for no upper limit).

        Returns:
            Validated float value.

        Raises:
            ValueError: If input is not a valid float or out of range.
        """
        while True:
            try:
                value = float(input(prompt))
                if value < min_val:
                    raise ValueError(
                        f"Value must be at least {min_val}."
                    )
                if max_val is not None and value > max_val:
                    raise ValueError(
                        f"Value must be at most {max_val}."
                    )
                return value
            except ValueError as e:
                if "must be" in str(e):
                    print(f"  ! {e}")
                else:
                    print("  ! Please enter a valid number.")
                continue

    def _prompt_yes_no(self, prompt: str) -> bool:
        """
        Prompt user for a yes/no answer.

        Args:
            prompt: Input prompt string.

        Returns:
            True for 'yes', False for 'no'.
        """
        while True:
            answer = input(prompt).strip().lower()
            if answer in ("y", "yes"):
                return True
            elif answer in ("n", "no"):
                return False
            else:
                print("  Please enter 'y' or 'n'.")


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="SDAI Calculator — Simplified Disease Activity "
        "Index for Rheumatoid Arthritis assessment.",
        epilog="Examples:\n"
        "  python -m src.sdai_calculator\n"
        "  python -m src.sdai_calculator --tjc 8 --sjc 6 "
        "--pga 5.0 --ega 4.0 --crp 2.5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--tjc", type=int, help="Tender Joint Count (0–28)"
    )
    parser.add_argument(
        "--sjc", type=int, help="Swollen Joint Count (0–28)"
    )
    parser.add_argument(
        "--pga",
        type=float,
        help="Patient Global Assessment on VAS (0–10 cm)",
    )
    parser.add_argument(
        "--ega",
        type=float,
        help="Evaluator Global Assessment on VAS (0–10 cm)",
    )
    parser.add_argument(
        "--crp",
        type=float,
        help="C-reactive protein level (mg/dL, >= 0)",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point with routing logic."""
    calculator = SDAICalculator()
    args = parse_arguments()

    cmd_args_provided = any([
        args.tjc is not None,
        args.sjc is not None,
        args.pga is not None,
        args.ega is not None,
        args.crp is not None,
    ])

    if cmd_args_provided:
        missing = []
        if args.tjc is None:
            missing.append("--tjc")
        if args.sjc is None:
            missing.append("--sjc")
        if args.pga is None:
            missing.append("--pga")
        if args.ega is None:
            missing.append("--ega")
        if args.crp is None:
            missing.append("--crp")

        if missing:
            print(
                f"Error: Missing required parameters: "
                f"{', '.join(missing)}"
            )
            print("Use --help for usage information.")
            sys.exit(1)

        try:
            calculator.print_detailed_result(
                args.tjc, args.sjc, args.pga, args.ega, args.crp
            )
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        console = InteractiveConsole(calculator)
        console.run()


if __name__ == "__main__":
    main()