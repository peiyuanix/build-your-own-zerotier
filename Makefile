CFLAGS = -I.
CFLAGS += -Werror=return-type

LDLIBS = -lpthread

HEADERS = sys_utils.h tap_utils.h
TARGETS = vport
VPORT_OBJS = vport.o tap_utils.o

all: ${TARGETS}

vport: ${VPORT_OBJS} $(HEADERS)

*.o: $(HEADERS)

clean:
	rm -f ${VPORT_OBJS} ${TARGETS}