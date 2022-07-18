
def calc_rsi(ex_rates, periods=14):
	change = ex_rates.diff()
	change.dropna(inplace=True)
	change_up = change.copy()
	change_down = change.copy()
	change_up[change_up<0] = 0
	change_down[change_down>0] = 0
	change.equals(change_up+change_down)
	avg_up = change_up.rolling(periods).mean()
	avg_down = change_down.rolling(periods).mean().abs()
	rsi = 100 * avg_up / (avg_up + avg_down)
	print(rsi.head(20))
	return rsi


def calc_mva(ex_rates, window):
	mav = ex_rates.rolling(int(window)).mean()
	return mav
