CC = gcc
CFLAGS = -mwindows -lgdiplus -I C:/ProgramData/mingw64/mingw64/x86_64-w64-mingw32/include
LDFLAGS = -L C:/ProgramData/mingw64/mingw64/x86_64-w64-mingw32/lib
TARGET = meu_jogo.exe
SOURCES = main.c tela.c
OBJECTS = $(SOURCES:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) -o $@ $(OBJECTS) $(CFLAGS) $(LDFLAGS)

%.o: %.c
	$(CC) -c $< -o $@ $(CFLAGS)

clean:
	rm -f $(OBJECTS) $(TARGET)