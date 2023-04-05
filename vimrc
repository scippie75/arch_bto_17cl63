syntax on
set tabstop=2 shiftwidth=2 expandtab
set backspace=indent,eol,start
set autoindent
set number
set nowrap
set path=~/projects/csp33d
map <F5> :tabp<CR>
map <F6> :tabn<CR>
map <F8> :A<CR>
map <F9> :!./m<CR>
map <C-F9> :!./m run<CR>
map <S-F9> :!./m debug<CR>
map <C-S-F9> :!./m valgrind<CR>
map <F10> :!./%<CR>
au BufNewFile,BufRead *.cpp set syntax=cpp11
au BufNewFile,BufRead *.c set syntax=cpp11
au BufRead *.fs set ft=
au BufRead *.vs set ft=

" Show tabs in light color
hi SpecialKey ctermfg=lightgray
set listchars=tab:>-
set list

let g:airline_powerline_fonts = 1
