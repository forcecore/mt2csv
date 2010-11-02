TMP=tmp

mt2csv: $(TMP)/mt.yy.cpp $(TMP)/mt.tab.cpp $(TMP)/mt.tab.hpp
	$(CXX) -o $@ $(TMP)/mt.tab.cpp $(TMP)/mt.yy.cpp 

$(TMP)/mt.tab.hpp: $(TMP)/mt.tab.cpp

$(TMP)/mt.tab.cpp: mt.y $(TMP)
	bison -o $@ $<

$(TMP)/mt.yy.cpp: mt.lex $(TMP)
	flex -o $@ $<

$(TMP):
	mkdir $(TMP)

clean:
	rm -rf $(TMP) mt2csv
