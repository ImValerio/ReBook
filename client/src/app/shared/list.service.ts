import { Injectable } from '@angular/core';
import { BehaviorSubject} from 'rxjs';

@Injectable()
export class ListService {

    sharedList: BehaviorSubject<any> = new BehaviorSubject<any>({});
    sharedList$ = this.sharedList.asObservable();

    setList(listText: any) {
        this.sharedList.next(listText);
    }

}