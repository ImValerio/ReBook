import { Component, OnDestroy, OnInit } from '@angular/core';
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
  
  
  private _unsubscribeAll: Subject<void> = new Subject<void>();

  constructor(private activatedRoute: ActivatedRoute, private searchResultService: SearchResultService, private listService: ListService){
  }

  ngOnInit(): void{
    this.searchtext = this.activatedRoute.snapshot.paramMap.get('text');
    
    this.listService.sharedList$.pipe(
      takeUntil(this._unsubscribeAll),
      ).subscribe((listValue)=>{
      // this.listText = listValue;
      // console.log(listValue);
      
      this.searchResult.next(listValue);
    });
    
    // this.listResult(this.searchtext);
  }

  // listResult(text: string| null): void {
  //   const t: SearchText ={
  //     text: text,
  //     mode: 'CONTENT_TEXT',
  //     page: 1
  //   };
  //   this.searchResultService.searchText(t).pipe(
  //     takeUntil(this._unsubscribeAll),
  //   ).subscribe((res) => {
  //     this.searchResult.next(res.results);
  //   });
  // }

  ngOnDestroy(): void{
    this._unsubscribeAll.next();
  }


}
