import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';

@Injectable()
export class ListService {

    sharedList: BehaviorSubject<any> = new BehaviorSubject<any>({});
    sharedList$ = this.sharedList.asObservable();

    constructor(){}

    setList(listText: any) {
        this.sharedList.next(listText);
    }

}