F:
cd F:\python\smallbowl1221\crawler_NCU\Mobile

for /l %%c in (0, 1, 18) do (
   python MO_Main.py %%c
)
pause