import data
import analysis

d = data.DATA(name="Amazon", ticker="AMZN")
a = analysis.ANALYSIS(data=d)

a.main()


