#include <stdint.h>
#include "smaz.h"

int decompress(void *src, void *dst, size_t src_len, size_t dst_len)
{
  uint16_t ctrl = 0;
  return;
}

void copy(char **out, off_t offset, int length)
{
    char *in = *out - offset;
    while (length-- >= 0) {
        * (++ (*out)) = * (in++);
    }
}

uint8_t next(char **in, uint16_t *ctrl)
{
    if (*ctrl & CTRL_END) {
        *ctrl <<= 1;
    } else {
        *ctrl = (((uint8_t)(*(*in) ++)) << 1) + 1;
        debug("ctrl:0x%02x\n",(*ctrl)>>1);
    }
    return *ctrl >> CTRL_NEXT_OFF & CTRL_NEXT_MASK;
}
