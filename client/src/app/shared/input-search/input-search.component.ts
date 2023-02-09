import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { debounceTime, map, Subject, take, takeUntil } from 'rxjs';
import { Book, SearchText } from 'src/app/models/search-text.model';
import { ListService } from '../list.service';
import { InputSearchService } from './input-search.service';

@Component({
  selector: 'input-search',
  templateUrl: './input-search.component.html',
  styleUrls: ['./input-search.component.scss'],
  providers: [
    InputSearchService,
  ]
})
export class InputSearchComponent implements OnInit, OnDestroy {

  @Input() initialText: string | null = '';
  @Input() initialMode: string | null = '';
  currentText= '';
  public listText: Book[] = [];
  public pageLength: number = 0;
  disableModeSelection: boolean = false;

  public modes = new Map<string,string>([['CONTENT_BM25','BM25'], ['CONTENT_TF_IDF', 'TF_IDF'], ['CONTENT_SENTIMENT', 'SENTIMENT'], ['CONTENT_CUSTOM', 'CUSTOM']]);
  selectedMode = 'CONTENT_BM25';
  actualMode: string = 'CONTENT_BM25';

  private listSearch: Subject<SearchText> = new Subject<SearchText>();
  private cancelCall: Subject<void> = new Subject<void>();
  private _unsubscribeAll: Subject<void> = new Subject<void>();

  constructor(private inputSearchService:InputSearchService, private router: Router, private listService: ListService){

  }

  ngOnInit(): void{
    if(this.initialText){
      this.currentText = this.initialText;
    }
    if(this.initialMode){
      this.selectedMode = this.initialMode;
    }      
    this.initializeListSearch();
  }

  loadList(): void{
    if(this.currentText){
      const book: SearchText ={
        text: this.currentText,
        mode: this.selectedMode,
        page: 1
      };
      this.listSearch.next(book);
    }else{
      this.cancelCall.next();
      this.listText = [];
    }
  }
  
  initializeListSearch(): void{
    this.listSearch.pipe(
      takeUntil(this._unsubscribeAll),
      debounceTime(200)
    ).subscribe((book)=>{
      this.cancelCall.next();
      this.inputSearchService.searchText(book).pipe(
        takeUntil(this._unsubscribeAll),
      ).subscribe((list) => {
        this.listService.pageLength = list.page_len;
        this.listText=list.results;
      });
    });
  }


  public outputTextResult(newText: string){
    const filterList = this.listText.filter(res => res.content===newText);
    if(this.actualMode !== this.selectedMode){
      this.actualMode = this.selectedMode;
      const book: SearchText ={
        text: newText,
        mode: this.selectedMode,
        page: 1
      };
      this.listService.mode = this.selectedMode;
      this.inputSearchService.searchText(book).pipe(
        takeUntil(this._unsubscribeAll),
      ).subscribe((list) => {
        this.listService.setList(list.results);
        this.router.navigate([ 'search-result', newText]);
      });
    }else{
      if(filterList.length>0){
        this.listService.setList(filterList);
      }else{
        this.listService.setList(this.listText);
      }
      this.listService.mode = this.selectedMode;
      this.router.navigate([ 'search-result', newText]);
    }
  }

  outputTextResultClick(bookReview: Book){
    this.listService.setList([bookReview]);
    this.listService.mode = this.selectedMode;
    this.router.navigate([ 'search-result', bookReview.content]);
  }

  ngOnDestroy(): void{
    this.cancelCall.next();
    this._unsubscribeAll.next();
  }

}
