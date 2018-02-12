map_kw_helper <- function(x, kw){
 tmpp <- lapply(x, tokens, what = "word", remove_punct = T, remove_symbols = T, remove_hyphens = T)
 tmpp <- tolower( unlist( tmpp[[1]] ) )
 tmpp <- tmpp[ !(tmpp %in% stopw) ]
	kwordss <- intersect(tmpp, kw)
 lengthh <- length(kwordss)
 return( list(kwordss= kwordss, lengthh= lengthh) )
}

map_kw <- function(x, ...) {
tmpp <- x %>% lapply(map_kw_helper, ... )
tmpp <- t( do.call(cbind, tmpp) )
sentence_number <- which(unlist(tmpp[,2])!=0)
keywords_in_sentence <- tmpp[sentence_number, 1]
tmp_dat <- data.frame(sentence_number= sentence_number, keywords_in_sentence= I(keywords_in_sentence) )
return(tmp_dat)
}