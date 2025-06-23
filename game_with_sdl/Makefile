CC = gcc
CFLAGS = -IC:\SDL3\SDL3-3.2.16\x86_64-w64-mingw32\include
LDFLAGS = -LC:\SDL3\SDL3-3.2.16\x86_64-w64-mingw32\lib -lSDL3
TARGET = jogo.exe
SRC = main.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) $(LDFLAGS) -o $(TARGET)

clean:
	rm -f $(TARGET)