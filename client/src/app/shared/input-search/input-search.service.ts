import { HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Subject, takeUntil} from 'rxjs';
import { SearchTextResults } from 'src/app/models/search-text.model';

@Injectable()
export class InputSearchService {

    private _unsubscribeAll: Subject<void> = new Subject<void>();

    constructor(private http: HttpClient){ }

    searchText(text: any){
        const url = 'http://localhost:8000/search';
        return this.http.post<SearchTextResults>(url, text).pipe(
            takeUntil(this._unsubscribeAll),
            // map(res => res.results)
        );
    }

}