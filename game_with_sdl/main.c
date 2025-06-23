#include <SDL3/SDL.h>
#include <SDL3/SDL_image.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#define WIDTH 800
#define HEIGHT 600

int main(int argc, char *argv[]) {

    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        fprintf(stderr, "SDL_Init failed: %s\n", SDL_GetError());
        return 1;
    }

    if (!IMG_Init()) {
        fprintf(stderr, "IMG_Init failed\n");
        SDL_Quit();
        return 1;
    }

    SDL_Window *win = SDL_CreateWindow("SDL Dino Game", WIDTH, HEIGHT, 0);
    if (!win) {
        fprintf(stderr, "SDL_CreateWindow failed: %s\n", SDL_GetError());
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    SDL_Renderer *ren = SDL_CreateRenderer(win, NULL);
    if (!ren) {
        fprintf(stderr, "SDL_CreateRenderer failed: %s\n", SDL_GetError());
        SDL_DestroyWindow(win);
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    SDL_Texture *bg = IMG_LoadTexture(ren, "img/textures-img/newchao.jpg");
    SDL_Texture *hero_idle = IMG_LoadTexture(ren, "img/hero-img/hero-initials.png");
    SDL_Texture *hero_run = IMG_LoadTexture(ren, "img/hero-img/hero-run1.png");
    SDL_Texture *hero_jump = IMG_LoadTexture(ren, "img/hero-img/hero-up.png");
    SDL_Texture *hero_down = IMG_LoadTexture(ren, "img/hero-img/hero-down.png");
    SDL_Texture *enemy_ground = IMG_LoadTexture(ren, "img/enemies-img/enemy3.png");
    SDL_Texture *enemy_air = IMG_LoadTexture(ren, "img/enemies-img/enemy1.png");

    if (!bg || !hero_idle || !hero_run || !hero_jump || !hero_down || !enemy_ground || !enemy_air) {
        fprintf(stderr, "Failed to load textures\n");
        SDL_DestroyTexture(bg);
        SDL_DestroyTexture(hero_idle);
        SDL_DestroyTexture(hero_run);
        SDL_DestroyTexture(hero_jump);
        SDL_DestroyTexture(hero_down);
        SDL_DestroyTexture(enemy_ground);
        SDL_DestroyTexture(enemy_air);
        SDL_DestroyRenderer(ren);
        SDL_DestroyWindow(win);
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    SDL_Rect hero = {100, HEIGHT - 120, 80, 100};
    SDL_Rect enemy = {WIDTH, HEIGHT - 100, 60, 80};
    SDL_Rect enemyFlying = {WIDTH + 300, HEIGHT - 200, 60, 60};

    int gravity = 0;
    bool jump = false, down = false, running = false, alive = true;

    SDL_Event e;
    Uint64 last = SDL_GetTicks(), now;

    while (alive) {
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_EVENT_QUIT) alive = false;
            else if (e.type == SDL_EVENT_KEY_DOWN) {
                const SDL_KeyboardEvent *key = &e.key;
                if (!running) running = true;
                if (key->keycode == SDLK_SPACE && !jump && !down) {
                    gravity = -20;
                    jump = true;
                }
                if (key->keycode == SDLK_DOWN && !jump) down = true;
            }
            else if (e.type == SDL_EVENT_KEY_UP) {
                const SDL_KeyboardEvent *key = &e.key;
                if (key->keycode == SDLK_DOWN) down = false;
            }
        }

        if (jump) {
            hero.y += gravity;
            gravity += 2;
            if (hero.y >= HEIGHT - 120) {
                hero.y = HEIGHT - 120;
                jump = false;
            }
        }

        enemy.x -= 10;
        if (enemy.x + enemy.w < 0) enemy.x = WIDTH + rand() % 200;

        enemyFlying.x -= 10;
        if (enemyFlying.x + enemyFlying.w < 0) enemyFlying.x = WIDTH + 400 + rand() % 200;

        SDL_Rect hero_box = hero;
        SDL_Rect ground_box = enemy;
        SDL_Rect air_box = enemyFlying;

        if (SDL_HasRectIntersection(&hero_box, &ground_box) && !jump && !down) alive = false;
        if (SDL_HasRectIntersection(&hero_box, &air_box) && !jump) alive = false;

        SDL_RenderClear(ren);
        SDL_RenderTexture(ren, bg, NULL, NULL);

        SDL_FRect hero_frect = { (float)hero.x, (float)hero.y, (float)hero.w, (float)hero.h };
        SDL_FRect enemy_frect = { (float)enemy.x, (float)enemy.y, (float)enemy.w, (float)enemy.h };
        SDL_FRect enemyFlying_frect = { (float)enemyFlying.x, (float)enemyFlying.y, (float)enemyFlying.w, (float)enemyFlying.h };

        if (!running) SDL_RenderTexture(ren, hero_idle, NULL, &hero_frect);
        else if (jump) SDL_RenderTexture(ren, hero_jump, NULL, &hero_frect);
        else if (down) SDL_RenderTexture(ren, hero_down, NULL, &hero_frect);
        else SDL_RenderTexture(ren, hero_run, NULL, &hero_frect);

        SDL_RenderTexture(ren, enemy_ground, NULL, &enemy_frect);
        SDL_RenderTexture(ren, enemy_air, NULL, &enemyFlying_frect);

        SDL_RenderPresent(ren);

        now = SDL_GetTicks();
        if (now - last < 16) SDL_Delay(16 - (now - last));
        last = now;
    }

    SDL_DestroyTexture(bg);
    SDL_DestroyTexture(hero_idle);
    SDL_DestroyTexture(hero_run);
    SDL_DestroyTexture(hero_jump);
    SDL_DestroyTexture(hero_down);
    SDL_DestroyTexture(enemy_ground);
    SDL_DestroyTexture(enemy_air);

    SDL_DestroyRenderer(ren);
    SDL_DestroyWindow(win);
    IMG_Quit();
    SDL_Quit();

    return 0;
}
