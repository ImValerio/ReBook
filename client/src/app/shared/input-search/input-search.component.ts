import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { Router } from '@angular/router';
import { debounceTime, Subject, takeUntil } from 'rxjs';
import { SearchText } from 'src/app/models/search-text.model';
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
  currentText= '';
  public listText: any[] = [];


  private listSearch: Subject<any> = new Subject<any>();
  private cancelCall: Subject<void> = new Subject<void>();
  private _unsubscribeAll: Subject<void> = new Subject<void>();

  constructor(private inputSearchService:InputSearchService, private router: Router, private listService: ListService){
  }

  ngOnInit(): void{
    
    if(this.initialText){
      this.currentText = this.initialText;
    }      
    this.initializeListSearch();
  }

  loadList(): void{
    if(this.currentText){
      const t: SearchText ={
        text: this.currentText,
        mode: 'CONTENT_TEXT',
        page: 1
      };
      this.listSearch.next(t);
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
        console.log(list.results);
        
        this.listText=list.results;
      });
    });
  }

  public outputTextResult(newText: any){
    const a = this.listText.filter(res => res.content===newText);
    if(a.length>0){
      this.listService.setList(a);
    }else{
      this.listService.setList(this.listText);
    }
    this.router.navigate([ 'search-result', newText]);
  }

  outputTextResultClick(newText: any){
    this.listService.setList([newText]);
    this.router.navigate([ 'search-result', newText.content]);
  }

  ngOnDestroy(): void{
    this.cancelCall.next();
    this._unsubscribeAll.next();
  }

}
