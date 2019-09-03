#include <stdint.h>
#include <stdio.h>

#ifdef DEBUG
#define debug(...) fprintf(stderr, ##__VA_ARGS__)
#else // DEBUG
#define debug(...)
#endif //DEBUG

int decompress(void *src, void *dst, size_t src_len, size_t dst_len);
void copy(char **out, off_t offset, int length);
uint8_t next(char **in, uint16_t *ctrl);
