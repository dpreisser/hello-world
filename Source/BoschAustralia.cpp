// BoschAustralia.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <string>

int _tmain(int argc, _TCHAR* argv[])

{
	int anInteger;

	/* 'R4' :R: 01.02.03.c */ anInteger = 1; char str1[] = "\'R4\' :R: 01.02.03.x";
	std::string str2 = "'R5' :R: 01.02.03.04.05.06";

	/* 'R4' :R: 01.02.03.d */
	std::cout << str1 << std::endl;

	if( 1 == anInteger ) 
	/* Another comment
	'R5' :R: 1.2.3.4.5.6
	'R5' :R: 1.2.3.4.5.7
	*/
	{

	std::cout << str2 << std::endl;

	}

	return 0;
}

