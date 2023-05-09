#ifndef _UTILS_H
#define _UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define ERROR_PRINT_THEN_EXIT(msg...) \
  fprintf(stderr, ##msg);       \
  exit(1);

#endif