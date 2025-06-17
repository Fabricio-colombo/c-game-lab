CC = gcc
CFLAGS = -mwindows
TARGET = meu_jogo.exe
SOURCES = main.c tela.c
OBJECTS = $(SOURCES:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) -o $@ $(OBJECTS) $(CFLAGS)

%.o: %.c
	$(CC) -c $< -o $@ $(CFLAGS)

clean:
	rm -f $(OBJECTS) $(TARGET)