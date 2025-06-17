#include "tela.h"
#include <objidl.h> // Para interfaces COM (usado pelo GDI+)
#pragma comment(lib, "gdiplus.lib")

// Função de callback para processar mensagens da janela
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    static GpBitmap* bitmap = NULL;
    static ULONG_PTR gdiplusToken;

    switch (uMsg) {
        case WM_CREATE: {
            // Inicializar GDI+
            GdiplusStartupInput gdiplusStartupInput;
            GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

            // Carregar a imagem PNG
            if (GdipCreateBitmapFromFile(L"img\\textures-img\\wallgray.png", &bitmap) != Ok) {
                MessageBoxW(NULL, L"Erro ao carregar wallgray.png!", L"Erro", MB_OK | MB_ICONERROR);
                bitmap = NULL;
            }
            return 0;
        }
        case WM_DESTROY: {
            // Liberar recursos
            if (bitmap) GdipDisposeImage((GpImage*)bitmap);
            GdiplusShutdown(gdiplusToken);
            PostQuitMessage(0);
            return 0;
        }
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            if (bitmap) {
                GpGraphics* graphics;
                GdipCreateFromHDC(hdc, &graphics);
                GdipDrawImageRectI(graphics, (GpImage*)bitmap, 0, 0, 800, 600); // Esticar para 800x600
                GdipDeleteGraphics(graphics);
            } else {
                // Fallback: fundo branco e retângulo vermelho
                FillRect(hdc, &ps.rcPaint, CreateSolidBrush(RGB(255, 255, 255)));
                HBRUSH redBrush = CreateSolidBrush(RGB(255, 0, 0));
                RECT rect = {100, 100, 150, 150};
                FillRect(hdc, &rect, redBrush);
                DeleteObject(redBrush);
            }
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