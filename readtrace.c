#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>


int main()  {
  
   int numtraces = 2;
   
    char *files[9]={"gromacs.log_l1misstrace_0","h264ref.log_l1misstrace_0","hmmer.log_l1misstrace_0","sphinx3.log_l1misstrace_1","sphinx3.log_l1misstrace_0","bzip2.log_l1misstrace_0","bzip2.log_l1misstrace_1","gcc.log_l1misstrace_0","gcc.log_l1misstrace_1"};
    int i;
    for(i=0;i<9;i++){
          FILE *fp;
          FILE *fp2;
         char a[100];
         strcpy(a,files[i]);
         strcat(a,".txt");
         fp2=fopen(a,"w+");
         fp = fopen( files[i], "rb");
         printf("%s\n",files[i]);
         assert(fp != NULL);
        char iord;
         char type;
         unsigned pc;
         unsigned long addr;

        while (!feof(fp)) {
         fread(&iord, sizeof(char), 1, fp);
         fread(&type, sizeof(char), 1, fp);
         fread(&addr, sizeof(unsigned long), 1, fp);
         fread(&pc, sizeof(unsigned), 1, fp);
         //fprintf(fp2, "%s %s %s %d", "We", "are", "in", 2012);
         if (type!=0)
              //printf("%d\n",type); 
              
             fprintf(fp2, "%ld\n", addr);
      }

      fclose(fp);
      fclose(fp2);
      printf("Done reading the files %s\n",a);

   }
 
 }   