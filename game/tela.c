#include "tela.h"

// Função de callback para processar mensagens da janela
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0); // Envia mensagem para fechar o programa
            return 0;
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            // Desenhar fundo branco
            FillRect(hdc, &ps.rcPaint, CreateSolidBrush(RGB(255, 255, 255)));
            // Desenhar retângulo vermelho
            HBRUSH redBrush = CreateSolidBrush(RGB(255, 0, 0));
            RECT rect = {100, 100, 150, 150}; // x, y, x+largura, y+altura
            FillRect(hdc, &rect, redBrush);
            DeleteObject(redBrush);
            EndPaint(hwnd, &ps);
            return 0;
        }
    }
    return DefWindowProcW(hwnd, uMsg, wParam, lParam);
}

HWND InicializarTela(HINSTANCE hInstance, int nCmdShow) {
    // Definir a classe da janela
    WNDCLASSW wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"JogoWin32";
    wc.hCursor = LoadCursorW(NULL, MAKEINTRESOURCEW(IDC_ARROW));
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);

    // Registrar a classe da janela
    if (!RegisterClassW(&wc)) {
        MessageBoxW(NULL, L"Erro ao registrar a classe da janela!", L"Erro", MB_OK | MB_ICONERROR);
        return NULL;
    }

    // Criar a janela
    HWND hwnd = CreateWindowExW(
        0, L"JogoWin32", L"Meu Jogo", WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL, NULL, hInstance, NULL
    );

    if (!hwnd) {
        MessageBoxW(NULL, L"Erro ao criar a janela!", L"Erro", MB_OK | MB_ICONERROR);
        return NULL;
    }

    // Exibir a janela
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    return hwnd;
}

int ExecutarLoopMensagens() {
    MSG msg = {0};
    while (GetMessageW(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessageW(&msg);
    }
    return (int)msg.wParam;
}