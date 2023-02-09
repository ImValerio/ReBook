import { Component, OnDestroy, OnInit } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { ActivatedRoute} from '@angular/router';
import { Observable, ReplaySubject, Subject, takeUntil } from 'rxjs';
import { Book, SearchText} from 'src/app/models/search-text.model';
import { ListService } from 'src/app/shared/list.service';
import { SearchResultService } from './search-result.service';

@Component({
  selector: 'search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss'],
  providers:[
    SearchResultService
  ],
})
export class SearchResultComponent implements OnInit, OnDestroy{

  searchtext: string | null= '';
  searchResult: ReplaySubject<Book[]> = new ReplaySubject<Book[]>(1);
  searchResult$: Observable<Book[]> = this.searchResult.asObservable();
  page: number = 0;
  length = 0;
  pageIndex = 0;
  
  private _unsubscribeAll: Subject<void> = new Subject<void>();

  constructor(private activatedRoute: ActivatedRoute, private searchResultService: SearchResultService, public listService: ListService){
  }

  ngOnInit(): void{
    this.searchtext = this.activatedRoute.snapshot.paramMap.get('text');
    this.listService.sharedList.pipe(
      takeUntil(this._unsubscribeAll),
      ).subscribe((listValue)=>{
          if(listValue.length){
            this.searchResult.next(listValue);
            this.length = this.listService.pageLength;
          }else{
            this.listResult(this.searchtext);
          }
    });    
  }

  listResult(text: string| null): void {
    const book: SearchText ={
      text: text,
      mode: this.listService.mode,
      page: (this.page+1)
    };
    this.searchResultService.searchText(book).pipe(
      takeUntil(this._unsubscribeAll),
    ).subscribe((res) => {
      if(res.results.length>0){
        this.searchResult.next(res.results);
      }else{
        this.searchResult.next(res.ngrams);
      }
      this.length = res.page_len;
    });
  }

  ngOnDestroy(): void{
    this._unsubscribeAll.next();
  }

  handlePageEvent(page:PageEvent): void{
    this.page = page.pageIndex;
    this.listResult(this.searchtext);
  }


}
