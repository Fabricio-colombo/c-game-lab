#include "tela.h"

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    HWND hwnd = InicializarTela(hInstance, nCmdShow);
    if (!hwnd) {
        return 1;
    }
    return ExecutarLoopMensagens();
}