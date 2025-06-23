#include <SDL3/SDL.h>

int main(void) {

    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window *janela = SDL_CreateWindow("SDL3 Teste", 800, 600, 0);
    SDL_Delay(3000);
    SDL_DestroyWindow(janela);
    SDL_Quit();
    return 0;
}
