# This function maps a set of keywords provided and returns the number of the sentence
# in which a keyword appears x is the text, and kw are the keywords provided

# This is a helper function We later use this function in the map_kw function
map_kw_helper <- function(x, kw) {
 tmpp <- lapply(x, tokens, what = "word", remove_punct = T, remove_symbols = T, remove_hyphens = T)
 tmpp <- tolower(unlist(tmpp[[1]]))  # convert to lower case
 tmpp <- tmpp[!(tmpp %in% stopw)]  # Remove stop words
 kwordss <- intersect(tmpp, kw)  # see if there are keywords which are left in the text
 lengthh <- length(kwordss)  # count how many (can also be zero)
 return(list(kwordss = kwordss, lengthh = lengthh))  # return the keywords and the length
}

# The function takes x which is the text and kw which will be passed to the
# map_kw_helper function
map_kw <- function(x, ...) {
 tmpp <- x %>% lapply(map_kw_helper, ...)  # apply the helper function to the text
 tmpp <- t(do.call(cbind, tmpp))  # make a matrix out of it
 sentence_number <- which(unlist(tmpp[, 2]) != 0)  # get the number of the sentence where keyword is mentioned
 keywords_in_sentence <- tmpp[sentence_number, 1]  # get which keywords are mentioned
 tmp_dat <- data.frame(sentence_number = sentence_number, keywords_in_sentence = I(keywords_in_sentence))  # make a data frame out of it
 return(tmp_dat)  # Return the data frame
}