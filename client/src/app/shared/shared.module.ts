import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatInputModule} from '@angular/material/input';

import {InputSearchComponent} from './input-search/input-search.component';
import {PageBodyComponent} from './layout/page-body/page-body.component';
import {PageHeaderComponent} from './layout/page-header/page-header.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { ListService } from './list.service';

@NgModule({
  declarations: [
    InputSearchComponent,
    PageBodyComponent,
    PageHeaderComponent,
    
  ],
  exports:[
    InputSearchComponent,
    PageBodyComponent,
    PageHeaderComponent,
    MatAutocompleteModule,
    MatInputModule,
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatAutocompleteModule,
    MatInputModule,
  ],
  providers: [
    ListService
  ]
})
export class SharedModule { }
