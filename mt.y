%{
	#include <cstdio>
	#include <string>
	#include <vector>
	#include "mt.tab.hpp"

	// prototypes to keep the compiler happy
	void yyerror (const char *error);
	int yyparse();
	int  yylex ();

	std::vector<std::string> g_vars;
	std::vector<double> g_vals;
%}

%defines
%token ID NUM SHARP
%union
{
	double dval;
	char * sval;
}

%type<dval> val
%type<sval> var


%%

mt: vars SHARP vals ;

vars: vars var | var ;
vals: vals val | val ;

var: ID  { g_vars.push_back( $$ ) };
val: NUM { g_vals.push_back( $$ ) };
