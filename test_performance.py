import pandas as pd
import numpy as np
import pytest
from performance import cagr, volatility, max_drawdown, alpha_beta, sortino_ratio, TRADING_DAYS_PER_YEAR

def test_cagr_double_en_un_an():
    # Arrange : je construis une entrée dont je connais le résultat attendu à l'avance
    dates = pd.bdate_range("2023-01-01", periods=252) # bdate pour business day
    cum_returns = pd.Series(np.linspace(1.0, 2.0, 252), index=dates)
    
    # Act : j'exécute la fonction à tester
    result = cagr(cum_returns)
    
    # Assert : je vérifie que le résultat correspond à ce que je sais être vrai
    assert result == pytest.approx(1.0)  # ~100% sur 1 an si la valeur double

def test_cagr_serie_vide_leve_erreur():
    empty_series = pd.Series([np.nan, np.nan, np.nan])
    
    with pytest.raises(ValueError):
        cagr(empty_series)

def test_volatility_serie_constante():
    # Arrange
    dates = pd.bdate_range("2023-01-01", periods=252)
    cte_series = pd.Series(1, index=dates)

    # Act
    result = volatility(cte_series)

    # Assert
    assert result == 0

def test_max_drawdown_serie_croissante():
    # Arrange
    incrs_series = pd.Series(np.arange(1,101))

    dates = pd.bdate_range("2023-01-01", periods=252)
    s = pd.Series(100 * (1.01) ** np.arange(252), index=dates) # On simule une croissance de 1% chaque jour

    # Act
    result1 = max_drawdown(incrs_series)
    result2 = max_drawdown(s)

    # Assert
    assert result1 == 0
    assert result2 == 0

def test_alpha_beta_contre_soi_meme():
    dates = pd.bdate_range("2023-01-01", periods=252)
    rdm_series = pd.Series(np.random.normal(size=252), index=dates)

    alpha, beta = alpha_beta(rdm_series, rdm_series, risk_free_rate=0)

    assert alpha == pytest.approx(0)
    assert beta == pytest.approx(1)

def test_sortino_prend_en_compte_les_zeros():
    dates = pd.bdate_range("2023-01-01", periods=1000)
    s = pd.Series(
    np.concatenate([
        np.full(100, -0.1),
        np.zeros(900)
    ]), 
    index=dates
    )

    # mauvais sortino
    downside_returns = s[s < 0]
    downside_returns_sigma = np.sqrt((downside_returns**2).mean())
    annual_downside_returns_sigma = downside_returns_sigma * np.sqrt(TRADING_DAYS_PER_YEAR)
    annual_R = s.mean() * TRADING_DAYS_PER_YEAR
    bad_result = annual_R / annual_downside_returns_sigma

    # bon sortino
    good_result = sortino_ratio(s)

    print("\nSortino","\nbad result =", bad_result, "\ngood result =", good_result)
    assert bad_result != good_result
    assert bad_result / good_result == pytest.approx(1/np.sqrt(10), rel=0.01) # car dans l'exemple choisi, n_bad = 100 et n_good = 1000 

