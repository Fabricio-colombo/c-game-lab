#ifndef TELA_H
#define TELA_H

#include <windows.h>
#include <gdiplus.h>
#include <objidl.h>

#pragma comment(lib, "gdiplus.lib")

// Função para inicializar e criar a janela
HWND InicializarTela(HINSTANCE hInstance, int nCmdShow);

// Função para executar o loop de mensagens
int ExecutarLoopMensagens();

#endif