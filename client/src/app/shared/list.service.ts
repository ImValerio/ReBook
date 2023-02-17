import { Injectable } from '@angular/core';
import { BehaviorSubject} from 'rxjs';
import { Book } from '../models/search-text.model';

@Injectable()
export class ListService {

    sharedList: BehaviorSubject<Book[]> = new BehaviorSubject<Book[]>([]);
    sharedList$ = this.sharedList.asObservable();
    pageLength: number=0;
    mode: string = '';
    // pageLength$ = this.pageLength.asObservable();

    setList(listText: any) {
        this.sharedList.next(listText);
    }

    // setPageLength(pageLength: number) {
    //     pageLength = 
    // }


}