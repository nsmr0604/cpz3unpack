;1
push eax
push ebx
push ecx
push edx
push ebp
push esi
push edi

;2
PUSH 1000
PUSH 0
CALL DWORD PTR DS:[501294] ;申请内存
mov edi,eax

;3
PUSH EDI                                 ; /Buffer
PUSH 780                                 ; |BufSize = 780 (1920.)
CALL DWORD PTR DS:[5010E4]               ; \GetCurrentDirectoryA

;4
PUSH cmvs5.005014EC                      ; /StringToAdd = "\image\"
PUSH EDI                                 ; |ConcatString
CALL DWORD PTR DS:[5010A8]               ; \lstrcatA

;5
MOV EBX,DWORD PTR SS:[ESP+94] ;文件名
PUSH EBX                                 ; /StringToAdd
PUSH EDI                                 ; |ConcatString
CALL DWORD PTR DS:[5010A8]               ; \lstrcatA

;计算字符串长度
PUSH EDI                                 ; /String
CALL DWORD PTR DS:[5010B8]               ; \lstrlenA

;替换扩展名
MOV DWORD PTR DS:[EDI+EAX-4],706D622E     ;".bmp"

;6
PUSH 0                                   ; /hTemplateFile = NULL
PUSH 10000080                            ; |Attributes = NORMAL|RANDOM_ACCESS
PUSH 3                                   ; |Mode = OPEN_EXISTING
PUSH 0                                   ; |pSecurity = NULL
PUSH 1                                   ; |ShareMode = FILE_SHARE_READ
PUSH 80000000                            ; |Access = GENERIC_READ
PUSH EDI                                 ; |FileName
CALL DWORD PTR DS:[5010CC]               ; \CreateFileA

;INVALID_HANDLE_VALUE=-1

CMP EAX,-1
JE SEG9

MOV ECX, EAX

;7
PUSH 0                                   ; /Origin = FILE_BEGIN
PUSH 0                                   ; |pOffsetHi = NULL
PUSH 36                                  ; |OffsetLo
PUSH EAX                                 ; |hFile
CALL DWORD PTR DS:[5010D4]               ; \SetFilePointer


MOV EBX,EBP被PUSH到的栈的位置，应该是DWORD PTR SS:[esp+14]

PUSH 0                                   ; /pOverlapped = NULL
MOV EDX,一块不用的内存                                                     ; |
PUSH EDX                                 ; |pBytesRead
PUSH EBX                                 ; |BytesToRead
PUSH ESI                                 ; |Buffer
PUSH ECX                                 ; |hFile
CALL DWORD PTR DS:[5010D0]               ; \ReadFile

;8

PUSH ECX                                 ; /hObject
CALL DWORD PTR DS:[5010C8]               ; \CloseHandle

;9
PUSH EDI                                 ; /hMemory
CALL DWORD PTR DS:[501160]               ; \LocalFree

;10
pop edi
pop esi
pop ebp
pop edx
pop ecx
pop ebx
pop eax


pop edi
mov eax,esi
pop esi
pop ebp
pop ebx
add esp,50
RETN 0C



;实际：

004FE976   > 50             PUSH EAX
004FE977   . 53             PUSH EBX
004FE978   . 51             PUSH ECX
004FE979   . 52             PUSH EDX
004FE97A   . 55             PUSH EBP
004FE97B   . 56             PUSH ESI
004FE97C   . 57             PUSH EDI
004FE97D   . 90             NOP
004FE97E   . 90             NOP
004FE97F   . 90             NOP
004FE980   . 90             NOP
004FE981   . 68 00100000    PUSH 1000                                ; /Size = 1000 (4096.)
004FE986   . 6A 00          PUSH 0                                   ; |Flags = LMEM_FIXED
004FE988   . FF15 94125000  CALL DWORD PTR DS:[<&KERNEL32.LocalAlloc>; \LocalAlloc
004FE98E   . 8BF8           MOV EDI,EAX
004FE990   . 57             PUSH EDI                                 ; /Buffer
004FE991   . 68 80070000    PUSH 780                                 ; |BufSize = 780 (1920.)
004FE996   . FF15 E4105000  CALL DWORD PTR DS:[<&KERNEL32.GetCurrent>; \GetCurrentDirectoryA
004FE99C   . 68 A7EA4F00    PUSH cmvs7.004FEAA7                      ; /StringToAdd = "\image\"
004FE9A1   . 57             PUSH EDI                                 ; |ConcatString
004FE9A2   . FF15 A8105000  CALL DWORD PTR DS:[<&KERNEL32.lstrcatA>] ; \lstrcatA
004FE9A8   . 90             NOP
004FE9A9   . 90             NOP
004FE9AA   . 8B9C24 9400000>MOV EBX,DWORD PTR SS:[ESP+94]
004FE9B1   . 53             PUSH EBX                                 ; /StringToAdd
004FE9B2   . 57             PUSH EDI                                 ; |ConcatString
004FE9B3   . FF15 A8105000  CALL DWORD PTR DS:[<&KERNEL32.lstrcatA>] ; \lstrcatA
004FE9B9   . 90             NOP
004FE9BA   . 90             NOP
004FE9BB   . 90             NOP
004FE9BC   . 57             PUSH EDI                                 ; /String
004FE9BD   . FF15 B8105000  CALL DWORD PTR DS:[<&KERNEL32.lstrlenA>] ; \lstrlenA
004FE9C3   . C74438 FC 2E62>MOV DWORD PTR DS:[EAX+EDI-4],706D622E
004FE9CB   . 90             NOP
004FE9CC   . 6A 00          PUSH 0                                   ; /hTemplateFile = NULL
004FE9CE   . 68 80000010    PUSH 10000080                            ; |Attributes = NORMAL|RANDOM_ACCESS
004FE9D3   . 6A 03          PUSH 3                                   ; |Mode = OPEN_EXISTING
004FE9D5   . 6A 00          PUSH 0                                   ; |pSecurity = NULL
004FE9D7   . 6A 01          PUSH 1                                   ; |ShareMode = FILE_SHARE_READ
004FE9D9   . 68 00000080    PUSH 80000000                            ; |Access = GENERIC_READ
004FE9DE   . 57             PUSH EDI                                 ; |FileName
004FE9DF   . FF15 CC105000  CALL DWORD PTR DS:[<&KERNEL32.CreateFile>; \CreateFileA
004FE9E5   . 83F8 FF        CMP EAX,-1
004FE9E8   . 74 3A          JE SHORT cmvs7.004FEA24
004FE9EA   . 90             NOP
004FE9EB   . 8BC8           MOV ECX,EAX
004FE9ED   . 90             NOP
004FE9EE   . 51             PUSH ECX
004FE9EF   . 6A 00          PUSH 0                                   ; /Origin = FILE_BEGIN
004FE9F1   . 6A 00          PUSH 0                                   ; |pOffsetHi = NULL
004FE9F3   . 6A 36          PUSH 36                                  ; |OffsetLo = 36 (54.)
004FE9F5   . 50             PUSH EAX                                 ; |hFile
004FE9F6   . FF15 D4105000  CALL DWORD PTR DS:[<&KERNEL32.SetFilePoi>; \SetFilePointer
004FE9FC   . 59             POP ECX
004FE9FD   . 90             NOP
004FE9FE   . 8BE9           MOV EBP,ECX
004FEA00   . 90             NOP
004FEA01   . 90             NOP
004FEA02   . 90             NOP
004FEA03   . 8B5C24 14      MOV EBX,DWORD PTR SS:[ESP+14]
004FEA07   . 6A 00          PUSH 0                                   ; /pOverlapped = NULL
004FEA09   . 8D0424         LEA EAX,DWORD PTR SS:[ESP]               ; |
004FEA0C   . 90             NOP                                      ; |
004FEA0D   . 50             PUSH EAX                                 ; |pBytesRead
004FEA0E   . 90             NOP                                      ; |
004FEA0F   . 53             PUSH EBX                                 ; |BytesToRead
004FEA10   . 56             PUSH ESI                                 ; |Buffer
004FEA11   . 51             PUSH ECX                                 ; |hFile
004FEA12   . FF15 D0105000  CALL DWORD PTR DS:[<&KERNEL32.ReadFile>] ; \ReadFile
004FEA18   . 90             NOP
004FEA19   . 90             NOP
004FEA1A   . 8BCD           MOV ECX,EBP
004FEA1C   . 90             NOP
004FEA1D   . 51             PUSH ECX                                 ; /hObject
004FEA1E   . FF15 C8105000  CALL DWORD PTR DS:[<&KERNEL32.CloseHandl>; \CloseHandle
004FEA24   > 57             PUSH EDI                                 ; /hMemory
004FEA25   . FF15 60115000  CALL DWORD PTR DS:[<&KERNEL32.LocalFree>>; \LocalFree
004FEA2B   . 90             NOP
004FEA2C   . 90             NOP
004FEA2D   . 5F             POP EDI
004FEA2E   . 5E             POP ESI
004FEA2F   . 5D             POP EBP
004FEA30   . 5A             POP EDX
004FEA31   . 59             POP ECX
004FEA32   . 5B             POP EBX
004FEA33   . 58             POP EAX
004FEA34   . 90             NOP
004FEA35   . 90             NOP
004FEA36   . 5F             POP EDI
004FEA37   . 8BC6           MOV EAX,ESI
004FEA39   . 5E             POP ESI
004FEA3A   . 5D             POP EBP
004FEA3B   . 5B             POP EBX
004FEA3C   . 83C4 50        ADD ESP,50
004FEA3F   . C2 0C00        RETN 0C







