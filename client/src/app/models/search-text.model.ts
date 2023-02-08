export interface SearchText {
    text: string | null;
    mode: string | null | undefined;
    page: number
}

export interface SearchTextResults{
    corrected: string;
    results: Book[];
    ngrams: Book[];
    dcg: number;
    page_len: number;
}

export interface Book{
    id: string;
    book_title: string;
    content: string;
    review_scrore: number;
    review_title: string;
    sentiment: number;
    length: number;
}

