#include "tela.h"
#include <objidl.h>
#pragma comment(lib, "gdiplus.lib")

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    static GpBitmap* background = NULL; // Fundo (wallgray.png)
    static GpBitmap* ground = NULL;     // Chão (chao.jpg)
    static ULONG_PTR gdiplusToken;

    switch (uMsg) {
        case WM_CREATE: {
            GdiplusStartupInput gdiplusStartupInput;
            GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
            // Carregar fundo
            if (GdipCreateBitmapFromFile(L"img\\textures-img\\wallgray.png", &background) != Ok) {
                MessageBoxW(NULL, L"Erro ao carregar wallgray.png!", L"Erro", MB_OK | MB_ICONERROR);
                background = NULL;
            }
            // Carregar chão
            if (GdipCreateBitmapFromFile(L"img\\textures-img\\waterchao.jpg", &ground) != Ok) {
                MessageBoxW(NULL, L"Erro ao carregar chao.jpg!", L"Erro", MB_OK | MB_ICONERROR);
                ground = NULL;
            }
            return 0;
        }
        case WM_DESTROY: {
            if (background) GdipDisposeImage((GpImage*)background);
            if (ground) GdipDisposeImage((GpImage*)ground);
            GdiplusShutdown(gdiplusToken);
            PostQuitMessage(0);
            return 0;
        }
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            if (background || ground) {
                GpGraphics* graphics;
                GdipCreateFromHDC(hdc, &graphics);
                // Desenhar fundo
                if (background) {
                    GdipDrawImageRectI(graphics, (GpImage*)background, 0, 0, 1400, 600);
                }
                // Desenhar chão (na parte inferior, altura 100px)
                if (ground) {
                    GdipDrawImageRectI(graphics, (GpImage*)ground, 0, 400, 1400, 200);
                }
                GdipDeleteGraphics(graphics);
            } else {
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
    WNDCLASSW wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"JogoWin32";
    wc.hCursor = LoadCursorW(NULL, MAKEINTRESOURCEW(IDC_ARROW));
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);

    if (!RegisterClassW(&wc)) {
        MessageBoxW(NULL, L"Erro ao registrar a classe da janela!", L"Erro", MB_OK | MB_ICONERROR);
        return NULL;
    }
    int xPos = (GetSystemMetrics(SM_CXSCREEN) - 1400) / 2;
    int yPos = (GetSystemMetrics(SM_CYSCREEN) - 600) / 2;
    HWND hwnd = CreateWindowExW(
        0, L"JogoWin32", L"Meu Jogo", WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT, 1400, 600,
        NULL, NULL, hInstance, NULL
    );

    if (!hwnd) {
        MessageBoxW(NULL, L"Erro ao criar a janela!", L"Erro", MB_OK | MB_ICONERROR);
        return NULL;
    }

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