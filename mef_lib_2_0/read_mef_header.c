/*
  read mef format file header (v.2) and display output

  To compile for a 64-bit intel system: (options will vary depending on your particular compiler and platform)
  Intel Compiler: icc read_mef_header.c mef_lib.c endian_functions.c AES_encryption.c RED_encode.c crc_32.c -o rmh -fast -m64
  GCC: gcc read_mef_header.c mef_lib.c endian_functions.c AES_encryption.c RED_encode.c crc_32.c -o rmh -O3 -arch x86_64

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#include "size_types.h"
#include "mef_header_2_0.h"
#include "RED_codec.h"
#include "mef_lib.h"


int main (int argc, const char * argv[]) {
  si4 i, num;
  char password[32];

  ui1 *bk_hdr;
  FILE *fp;
  MEF_HEADER_INFO header;

  if (argc < 2 || argc > 3)
  {
    (void) printf("USAGE: %s file_name [password] \n", argv[0]);
    return(1);
  }

  *password = 0;

  if (argc > 2)
  {
    //check password length
    if (strlen(argv[2]) > 16) {
      fprintf(stderr, "Error: Password cannot exceed 16 characters\n");
      return 1;
    }
    sprintf(password, argv[2]);
  }


  fp = fopen(argv[1], "r");
  if (fp == NULL) {
      fprintf(stderr, "Error opening file %s\n", argv[1]);
      return 1;
    }

  bk_hdr = calloc(sizeof(ui1), MEF_HEADER_LENGTH);
  num = fread(bk_hdr, 1, MEF_HEADER_LENGTH, fp);
  if (num != MEF_HEADER_LENGTH) {
    fprintf(stderr, "Error reading file %s\n", argv[1]);
    return 1;
  }

  (void)read_mef_header_block(bk_hdr, &header, password);
  showHeader(&header);


  free(bk_hdr);
  return 0;
}
