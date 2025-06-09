" general settings
let mapleader = " "             " set leader key to space

if ! filereadable(system('echo -n "${XDG_CONFIG_HOME:-$HOME/.config}/nvim/autoload/plug.vim"'))
	echo "Downloading junegunn/vim-plug to manage plugins..."
	silent !mkdir -p ${XDG_CONFIG_HOME:-$HOME/.config}/nvim/autoload/
	silent !curl "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim" > ${XDG_CONFIG_HOME:-$HOME/.config}/nvim/autoload/plug.vim
	autocmd VimEnter * PlugInstall
endif

set title
set path+=**                    " searches current directory recursively.
set nocompatible                " necessary for several cool vim things
set tabstop=4 softtabstop=4     " sets tabs equal to 4 spaces
set shiftwidth=4                " sets shift width to 4 spaces
set expandtab                   " converts tabs to spaces
set smartindent                 " attempts to properly indent
set showcmd                     " shows current command
set showmode                    " shows current mode
filetype plugin on
syntax on                       " enables syntax highlighting
set number                      " shows line numbers
set relativenumber              " shows line numbers relative to the cursor position
set nowrap                      " does not allow lines to wrap
set ignorecase                  " ignores case when searching
set smartcase                   " turns on case sensitive search when letters are capitalized
set incsearch                   " sets incremental search
set scrolloff=8                 " starts scrolling the page when cursor is # lines from the bottom
set encoding=utf-8
set nohlsearch                  " turns off highlight after enter is pressed when searching
set mouse=a                     " mouse scrolling
set clipboard+=unnamedplus      " sets the clipboard so you can paste stuff from outside vim into vim.
set complete+=kspell            " auto complete with spellcheck
set completeopt=menuone,longest " auto complete menu (It's pretty great)
set splitbelow splitright       " sets split behavior
set laststatus=2                " always show statusline

" PLUGINS

call plug#begin()
" ColorScheme and theme
Plug 'https://github.com/folke/tokyonight.nvim'

" File Manager incorporation
Plug 'https://github.com/vifm/vifm.vim'

" Syntax Highlighting
Plug 'https://github.com/vim-python/python-syntax'
Plug 'https://github.com/kovetskiy/sxhkd-vim'
"Plug 'https://github.com/PotatoesMaster/i3-vim-syntax'
Plug 'https://github.com/rust-lang/rust.vim'
Plug 'https://github.com/yuezk/vim-js'
Plug 'https://github.com/maxmellon/vim-jsx-pretty'

" Preview colors in vim
Plug 'https://github.com/ap/vim-css-color'

" vim autocomplete
Plug 'vim-scripts/AutoComplPop'

call plug#end()

colorscheme retrobox     " Sets the ColorScheme

" Make background transparent

highlight Normal guibg=none
highlight NonText guibg=none
highlight Normal ctermbg=none
highlight NonText ctermbg=none

" remap split navigation to just CTRL + hjkl
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" adjust split sizes easier
noremap <silent> <C-Left> :vertical resize +3<CR>
noremap <silent> <C-Right> :vertical resize -3<CR>
noremap <silent> <C-Up> :resize -3<CR>
noremap <silent> <C-Down> :resize +3<CR>

" open a terminal inside nvim
map <leader>tt :vnew term://bash<CR>

" change 2 split windows from vertical to horizontal or vice versa
map <leader>th <C-w>t<C-w>H
map <leader>tk <C-w>t<C-w>K

" remap ESC to ii
:imap CapsLock <Esc>
:imap ii <Esc>
:imap jk <Esc>
:imap kj <Esc>

" open vifm in a vertical split
nnoremap <leader>vs :VsplitVifm<CR>

" remove  trailing whitespace on save
autocmd BufWritePre * %s/\s\+$//e

" automatically close brackets and parenthesis and place cursor inside
inoremap " ""<left>
inoremap ' ''<left>
inoremap ( ()<left>
inoremap [ []<left>
inoremap { {}<left>
inoremap {<CR> {<CR>}<ESC>0
inoremap {;<CR> {<CR>};<ESC>0

" Save file as sudo on files that require root permission
	cabbrev w!! execute 'silent! write !doas tee % >/dev/null' <bar> edit!
