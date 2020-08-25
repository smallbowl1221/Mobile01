call activate NCU

D:

cd D:\python\crawler_NCU\Mobile

for /l %%c in (0, 1, 18) do (
   python MO_Main.py %%c
)

call conda deactivate

pause