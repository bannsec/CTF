color herald

set tabstop=4
set expandtab
set shiftwidth=4
set background=dark

map <C-n> <C-w><C-w>

syntax on
filetype indent plugin on

" Pretty tab line colors
hi TabLineSel ctermfg=LightBlue
hi TabLine ctermfg=White

" highlight current line number
hi clear CursorLine
hi CursorLineNR ctermbg=Blue ctermfg=White cterm=bold guibg=blue gui=bold
set cursorline
set number
set incsearch
set hlsearch

execute pathogen#infect()

" Always open nerd tree
"autocmd vimenter * NERDTree

" If we open vim by itself, pop up nerd tree
"autocmd StdinReadPre * let s:std_in=1
"autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif

" Only window left is nerd tree? kill it
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif

" Auto open nerd tree when vim opening a directory
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists("s:std_in") | exe 'NERDTree' argv()[0] | wincmd p | ene | endif

map <C-t> :NERDTreeToggle<CR>

" Custom overrides for transparent background
hi Normal guibg=NONE ctermbg=NONE
hi NonText guibg=NONE ctermbg=NONE
"hi Include ctermfg=177 guifg=#BF81FA guisp=#1F1F1F ctermbg=NONE guibg=NONE
hi Include ctermbg=NONE guibg=NONE
hi String ctermbg=NONE guibg=NONE
hi SpecialKey ctermbg=NONE guibg=NONE
hi NonText ctermbg=NONE guibg=NONE
hi Directory ctermbg=NONE guibg=NONE
hi ErrorMsg ctermbg=NONE guibg=NONE
hi IncSearch ctermbg=NONE guibg=NONE
hi Search ctermbg=NONE guibg=NONE
hi MoreMsg ctermbg=NONE guibg=NONE
hi ModeMsg ctermbg=NONE guibg=NONE
hi LineNr ctermbg=NONE guibg=NONE
hi Question ctermbg=NONE guibg=NONE
"hi StatusLine ctermbg=NONE guibg=NONE
"hi StatusLineNC ctermbg=NONE guibg=NONE
hi VertSplit ctermbg=NONE guibg=NONE
hi Title ctermbg=NONE guibg=NONE
hi Visual ctermbg=NONE guibg=NONE
hi VisualNOS ctermbg=NONE guibg=NONE
hi WarningMsg ctermbg=NONE guibg=NONE
hi WildMenu ctermbg=NONE guibg=NONE
hi Folded ctermbg=NONE guibg=NONE
hi FoldColumn ctermbg=NONE guibg=NONE
hi DiffAdd ctermbg=NONE guibg=NONE
hi DiffChange ctermbg=NONE guibg=NONE
hi DiffDelete ctermbg=NONE guibg=NONE
hi DiffText ctermbg=NONE guibg=NONE
hi SignColumn ctermbg=NONE guibg=NONE
hi Conceal ctermbg=NONE guibg=NONE
hi SpellBad ctermbg=NONE guibg=NONE
hi SpellCap ctermbg=NONE guibg=NONE
hi SpellRare ctermbg=NONE guibg=NONE
hi SpellLocal ctermbg=NONE guibg=NONE
hi Pmenu ctermbg=NONE guibg=NONE
hi PmenuSel ctermbg=NONE guibg=NONE
hi PmenuSbar ctermbg=NONE guibg=NONE
hi PmenuThumb ctermbg=NONE guibg=NONE
hi TabLine ctermbg=NONE guibg=NONE
hi TabLineSel ctermbg=NONE guibg=NONE
hi TabLineFill ctermbg=NONE guibg=NONE
hi CursorColumn ctermbg=NONE guibg=NONE
hi ColorColumn ctermbg=NONE guibg=NONE
hi MatchParen ctermbg=NONE guibg=NONE
hi Comment ctermbg=NONE guibg=NONE
hi Constant ctermbg=NONE guibg=NONE
hi Special ctermbg=NONE guibg=NONE
hi Identifier ctermbg=NONE guibg=NONE
hi Statement ctermbg=NONE guibg=NONE
hi PreProc ctermbg=NONE guibg=NONE
hi Type ctermbg=NONE guibg=NONE
hi Underlined ctermbg=NONE guibg=NONE
hi Ignore ctermbg=NONE guibg=NONE
hi Error ctermbg=NONE guibg=NONE
hi Todo ctermbg=NONE guibg=NONE
hi String ctermbg=NONE guibg=NONE
hi Character ctermbg=NONE guibg=NONE
hi Number ctermbg=NONE guibg=NONE
hi Boolean ctermbg=NONE guibg=NONE
hi Function ctermbg=NONE guibg=NONE
hi Conditional ctermbg=NONE guibg=NONE
hi Repeat ctermbg=NONE guibg=NONE
hi Label ctermbg=NONE guibg=NONE
hi Operator ctermbg=NONE guibg=NONE
hi Keyword ctermbg=NONE guibg=NONE
hi Exception ctermbg=NONE guibg=NONE
hi Include ctermbg=NONE guibg=NONE
hi Define ctermbg=NONE guibg=NONE
hi Macro ctermbg=NONE guibg=NONE
hi PreCondit ctermbg=NONE guibg=NONE
hi StorageClass ctermbg=NONE guibg=NONE
hi Structure ctermbg=NONE guibg=NONE
hi Typedef ctermbg=NONE guibg=NONE
hi Tag ctermbg=NONE guibg=NONE
hi SpecialChar ctermbg=NONE guibg=NONE
hi Delimiter ctermbg=NONE guibg=NONE
hi SpecialComment ctermbg=NONE guibg=NONE
hi Debug ctermbg=NONE guibg=NONE
hi Normal ctermbg=NONE guibg=NONE

