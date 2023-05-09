#ifndef __TUNTAP_H
#define __TUNTAP_H

#include <linux/if.h>
#include <linux/if_tun.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>
#include <unistd.h>

int tap_alloc(char *dev);

#endif