@echo off
setlocal
pushd "%~dp0\..\paper" >NUL 2>&1
REM Clean auxiliary files (optional)
del /Q main.aux main.out main.toc main.log main.synctex.gz main.fls main.fdb_latexmk 2>NUL
echo [1/2] pdflatex main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex >NUL
if errorlevel 1 goto :err
echo [2/2] pdflatex main.tex (second pass)
pdflatex -interaction=nonstopmode -halt-on-error main.tex >NUL
if errorlevel 1 goto :err
echo PDF built: %CD%\main.pdf
popd >NUL 2>&1
exit /b 0

:err
echo.
echo Build failed. Showing last 50 lines of log:
for /f "skip=0 delims=" %%L in ('powershell -NoLogo -Command "(Get-Content -Path main.log -Tail 50) -join \"`n\""') do @echo %%L
popd >NUL 2>&1
exit /b 1

