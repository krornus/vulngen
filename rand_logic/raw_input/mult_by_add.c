#include <stdio.h>
 
int main()
{
    int i,j;
    int k;
    int l;
     
    i = num1;
    j = num2;
    k=num3;
    for(l=num4;l<=j;l++){
        k += i;
    }
    printf("%d%d%d\n",i,j,k);
    return 0;
}
