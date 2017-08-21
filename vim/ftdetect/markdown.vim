autocmd BufNewFile *.mkd,*.md exec ":call SetMKDTitle()"
" map the SetLastModifiedTime command automatically  
au BufWrite *.mkd,*.md call SetMKDLastModifiedTime()

set textwidth=0

" 定义函数 SetTitle, 自动插入文件头模板
" Title: 
" Slug: 
" Date: 
" Tags: 
"
" [TOC]
func! SetMKDTitle()
    call setline(1, "Title: ".expand("%:r"))  
    call setline(2, "Slug:   ")  
    call setline(3, "Date: ".strftime("%c"))  
    call setline(4, "Authors: sndnyang sndnyang.github.io")  
    call setline(5, "Modified: ".strftime("%c"))  
    call setline(6, "Category:   ")  
    call setline(7, "Tags:   ")  
    call setline(8, "Summary:   ")  
    call setline(9, "")  
    call setline(10,"[TOC]") 
endfunc

function! SetMKDLastModifiedTime()
    let lineno = 0
    let modif_time = strftime("%c")  
    for i in range(1, 8)
        let line = getline(i)

        if line =~ '^Modified:'
            let line = substitute(line,':\s.*', ': '.modif_time, "")
            call setline(i, line)  
            break
        endif  
    endfor
endfunction 
