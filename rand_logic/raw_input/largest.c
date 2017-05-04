#include <stdio.h>
 
int main()
{ 
    int i,j,k;
    int l;
    i = num1;
    j=num2;
    k=num3;
    if(i>j && i>k)        
        l=i;
    else if(j>i && j>k)       
        l=j;
    else
        l=k;
    printf("%d\n",l);
    return 0;
}