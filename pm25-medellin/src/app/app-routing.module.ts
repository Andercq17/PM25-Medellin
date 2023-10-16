import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SimulacionComponent } from './components/simulacion/simulacion.component';
import { HomeComponent } from './components/home/home.component';

const routes: Routes = [
  { path: 'simulacion', component: SimulacionComponent },
  { path: 'home', component: HomeComponent },
  { path: '', component: HomeComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
