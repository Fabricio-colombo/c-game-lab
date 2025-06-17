#include "tela.h"

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Inicializar a tela
    HWND hwnd = InicializarTela(hInstance, nCmdShow);
    if (!hwnd) {
        return 1;
    }

    // Executar o loop de mensagens
    return ExecutarLoopMensagens();
}