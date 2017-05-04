#include <stdio.h>

int main()
{
	int i, j;
	int k, l;

	i=num1;
	j=num2;
	
	k= i/j;
	l= i%j;
	l += (i-j);
	k -= (k*i);
		
	printf("%d%d\n",k,l);
	
	return 0;
}
