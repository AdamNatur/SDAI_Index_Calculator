"""Tests for SDAI Calculator."""

import pytest
from src.sdai_calculator import ActivityCategory, SDAICalculator


class TestSDAICalculator:
    """Test suite for SDAICalculator class."""

    @pytest.fixture
    def calculator(self) -> SDAICalculator:
        """Create a fresh calculator instance for each test."""
        return SDAICalculator()

    # ------------------ Calculation Tests ------------------

    def test_remission(self, calculator: SDAICalculator) -> None:
        """Test remission classification."""
        result = calculator.calculate(
            tjc=0, sjc=0, pga=0.5, ega=0.5, crp=0.2
        )
        assert result["sdai"] == 1.2
        assert result["category"] == ActivityCategory.REMISSION

    def test_low_activity(self, calculator: SDAICalculator) -> None:
        """Test low activity classification."""
        result = calculator.calculate(
            tjc=3, sjc=2, pga=2.0, ega=1.5, crp=0.8
        )
        assert result["sdai"] == 9.3
        assert result["category"] == ActivityCategory.LOW

    def test_moderate_activity(self, calculator: SDAICalculator) -> None:
        """Test moderate activity classification."""
        result = calculator.calculate(
            tjc=8, sjc=6, pga=5.0, ega=4.0, crp=2.5
        )
        assert result["sdai"] == 25.5
        assert result["category"] == ActivityCategory.MODERATE

    def test_high_activity(self, calculator: SDAICalculator) -> None:
        """Test high activity classification."""
        result = calculator.calculate(
            tjc=15, sjc=12, pga=8.0, ega=7.0, crp=4.5
        )
        assert result["sdai"] == 46.5
        assert result["category"] == ActivityCategory.HIGH

    # ------------------ Boundary Tests ------------------

    def test_exact_remission_threshold(
        self, calculator: SDAICalculator
    ) -> None:
        """Test exactly at remission threshold (3.3)."""
        result = calculator.calculate(
            tjc=0, sjc=1, pga=1.0, ega=1.0, crp=0.3
        )
        assert result["category"] == ActivityCategory.REMISSION

    def test_exact_low_threshold(
        self, calculator: SDAICalculator
    ) -> None:
        """Test exactly at low activity threshold (11.0)."""
        result = calculator.calculate(
            tjc=3, sjc=3, pga=2.0, ega=2.0, crp=1.0
        )
        assert result["category"] == ActivityCategory.LOW

    def test_exact_moderate_threshold(
        self, calculator: SDAICalculator
    ) -> None:
        """Test exactly at moderate activity threshold (26.0)."""
        result = calculator.calculate(
            tjc=8, sjc=8, pga=5.0, ega=4.0, crp=1.0
        )
        assert result["category"] == ActivityCategory.MODERATE

    def test_zero_values(self, calculator: SDAICalculator) -> None:
        """Test with all zero values."""
        result = calculator.calculate(
            tjc=0, sjc=0, pga=0.0, ega=0.0, crp=0.0
        )
        assert result["sdai"] == 0.0
        assert result["category"] == ActivityCategory.REMISSION

    def test_maximum_values(self, calculator: SDAICalculator) -> None:
        """Test with maximum allowed joint counts and VAS."""
        result = calculator.calculate(
            tjc=28, sjc=28, pga=10.0, ega=10.0, crp=15.0
        )
        assert result["sdai"] == 91.0
        assert result["category"] == ActivityCategory.HIGH

    # ------------------ Validation Tests ------------------

    def test_tjc_too_high(self, calculator: SDAICalculator) -> None:
        """Test TJC above maximum."""
        with pytest.raises(ValueError, match="TJC.*outside range"):
            calculator.calculate(tjc=29, sjc=5, pga=5.0, ega=5.0, crp=1.0)

    def test_sjc_negative(self, calculator: SDAICalculator) -> None:
        """Test negative SJC value."""
        with pytest.raises(ValueError, match="SJC.*outside range"):
            calculator.calculate(tjc=5, sjc=-1, pga=5.0, ega=5.0, crp=1.0)

    def test_pga_above_maximum(self, calculator: SDAICalculator) -> None:
        """Test PGA above 10.0."""
        with pytest.raises(ValueError, match="PGA.*outside range"):
            calculator.calculate(
                tjc=5, sjc=5, pga=10.5, ega=5.0, crp=1.0
            )

    def test_ega_negative(self, calculator: SDAICalculator) -> None:
        """Test negative EGA value."""
        with pytest.raises(ValueError, match="EGA.*outside range"):
            calculator.calculate(
                tjc=5, sjc=5, pga=5.0, ega=-0.1, crp=1.0
            )

    def test_crp_negative(self, calculator: SDAICalculator) -> None:
        """Test negative CRP value."""
        with pytest.raises(ValueError, match="CRP.*outside range"):
            calculator.calculate(
                tjc=5, sjc=5, pga=5.0, ega=5.0, crp=-0.1
            )

    # ------------------ Interpretation Tests ------------------

    def test_interpretation_string(self, calculator: SDAICalculator) -> None:
        """Test that interpretation string is correctly formatted."""
        result = calculator.calculate(
            tjc=8, sjc=6, pga=5.0, ega=4.0, crp=2.5
        )
        assert "SDAI =" in result["interpretation"]
        assert "Moderate Activity" in result["interpretation"]

    # ------------------ Enum Tests ------------------

    def test_enum_values(self) -> None:
        """Test that ActivityCategory enum values are correct."""
        assert ActivityCategory.REMISSION.value == "Remission"
        assert ActivityCategory.LOW.value == "Low Activity"
        assert ActivityCategory.MODERATE.value == "Moderate Activity"
        assert ActivityCategory.HIGH.value == "High Activity"

    def test_enum_membership(self) -> None:
        """Test enum membership and iteration."""
        categories = list(ActivityCategory)
        assert len(categories) == 4
        assert ActivityCategory.REMISSION in categories