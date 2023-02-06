import { Component, OnDestroy, OnInit } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { ActivatedRoute} from '@angular/router';
import { Observable, ReplaySubject, Subject, takeUntil } from 'rxjs';
import { SearchText, SearchTextResults } from 'src/app/models/search-text.model';
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
  searchResult: ReplaySubject<any> = new ReplaySubject<any>(1);
  searchResult$: Observable<any> = this.searchResult.asObservable();
  page: number = 0;
  length = 50;
  pageSize = 10;
  pageIndex = 0;
  
  
  private _unsubscribeAll: Subject<void> = new Subject<void>();

  constructor(private activatedRoute: ActivatedRoute, private searchResultService: SearchResultService, private listService: ListService){
  }

  ngOnInit(): void{
    this.searchtext = this.activatedRoute.snapshot.paramMap.get('text');
    
    this.listService.sharedList$.pipe(
      takeUntil(this._unsubscribeAll),
      ).subscribe((listValue)=>{
        if(listValue.length){
          this.searchResult.next(listValue);
        }else{
          this.listResult(this.searchtext);
        }      
    });
  }

  listResult(text: string| null): void {
    const t: SearchText ={
      text: text,
      mode: 'CONTENT_TEXT',
      page: (this.page+1)
    };
    this.searchResultService.searchText(t).pipe(
      takeUntil(this._unsubscribeAll),
    ).subscribe((res) => {
      this.searchResult.next(res.results);
    });
  }

  ngOnDestroy(): void{
    this._unsubscribeAll.next();
  }

  handlePageEvent(page:PageEvent): void{
    console.log('sono dentro', page);
    this.page = page.pageIndex;
    this.listResult(this.searchtext);
  }


}
