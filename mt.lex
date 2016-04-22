%{
	#include <cstdio>
	#include <cassert>
	#include <string>
	#include <vector>
	#include "mt.tab.hpp"
	int yyparse();

	extern std::vector<std::string> g_vars;
	extern std::vector<double> g_vals;
%}

%%

[\t\n ]	continue;
^"$".+	continue;
^".TITLE".+	continue;
"#" { return SHARP; }
[a-zA-Z][^#[:space:]]* { yylval.sval = yytext ; return ID; }
[0-9]+("."[0-9]+)? { yylval.dval = atof(yytext) ; return NUM; }
[0-9]+("."[0-9]+(e-[0-9]+)?)? { yylval.dval = atof(yytext) ; return NUM; }

%%
int yywrap(void)
{
	return 1;
}

void yyerror( const char * s )
{
	fprintf( stderr, "%s\n", s );
}

int main()
{
	yyparse();

	assert( g_vars.size() == g_vals.size() );

	for( int i = 0 ; i < g_vars.size() ; ++i ) {
		printf( "%s,%g\n", g_vars[i].c_str(), g_vals[i] );
	}
	return 0;
}
