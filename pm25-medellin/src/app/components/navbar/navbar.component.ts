import { Component,HostListener,ElementRef, Renderer2 } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent {
  scrollYPosition:number=0;
  bandera:boolean=false;
  divStyles: any = {};
  
  constructor(private renderer: Renderer2, private el: ElementRef) {}

  @HostListener("window:scroll", ['$event'])
  doSomethingOnWindowsScroll(event:Event):void{
    this.scrollYPosition = window.scrollY;
    if (this.scrollYPosition > 1 && this.bandera!=true) {
      this.bandera = true;
      this.divStyles = {
        'transition': 'all 0.2s ease-in-out',
        'box-shadow': '0 0px 10px black',
      };
    } else if(this.scrollYPosition==0) {
      if (this.bandera) {
        this.bandera = false;
        this.divStyles = {};
      }
    }
  }
}
